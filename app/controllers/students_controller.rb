# -*- encoding : utf-8 -*-
class StudentsController < ApplicationController

  skip_before_filter :authenticate_user!, :only => :api
  skip_before_filter :verify_authenticity_token, :only => :api
  before_filter :verify_api_key, :only => :api

  def multi_search
    @event   = Event.find(params[:event_id], :include => :ticket_types)
    @student = Studentkoll.where(:rfidnr => params[:student][:atr]).first

    unless @student
      @message = "Hittade ingen student!"
    end

    if @student && @event.autosave?
      @registration  = @event.register_student(@student, @event.available_ticket_types, current_user)
      @tickets = @registration.tickets
      @visitor = @registration.visitor
      @program = Program.for(@student.liu_id)
      @message = "#{@student} (#{@program}) har registrerats"
    end
  rescue ActiveRecord::RecordInvalid => e
    errors = e.record.errors

    if @student
      @message = "Kunde inte registrera #{@student} på grund av: "
    else
      @message  = "Kunde registrera på grund av: "
    end
    @message += errors.keys.collect {|k| errors[k] }.flatten.collect {|k| k.capitalize }.join(', ')
  end

  def search
    @event    = Event.find(params[:event_id], :include => :ticket_types)
    @students = Studentkoll.search(params[:student][:query])
    @students_count = @students.count

    # Check in StureStudent if Studentkoll couldn't be found
    # FIXME Should check Sture
    if @students_count == 0
      @students = StureStudent.search(params[:student][:query])
      @students_count = @students.count
    end

    if @students_count == 1
      @student = @students.first

      if @student.union_member?
        if @event.permanent?
          @status = :success
        end
        @message = "#{@student} är medlem i #{@student.union}"
      else
        if @event.permanent?
          @status = :failure
        end
        @message = "#{@student} är inte kårmedlem"
      end

      # Should we autosave the student?
      if @event.autosave?
        @registration  = @event.register_student(@student, @event.available_ticket_types, current_user)
        @tickets = @registration.tickets
        @visitor = @registration.visitor
        unless @event.permanent?
          @message += ' och har registrerats'
        end
      else
        # Maybe look for existing user?
        @visitor = Visitor.where(:personal_number => @student.personal_number).first
      end
    else
      @status = :failure
      @message = 'Hittade ingen student.'
    end
  rescue ActiveRecord::RecordInvalid => e
    errors = e.record.errors

    @status   = :failure
    @message  = "Kunde registrera på grund av: "
    @message += errors.keys.collect {|k| errors[k] }.flatten.collect {|k| k.capitalize }.join(', ')
  ensure
    # If we're using autosave, render tickets/sale right away
    if @event.autosave?
      render 'tickets/sale'
    end
  end

  def search_card
    @event = Event.find(params[:event_id], :include => :ticket_types)
    @student = Studentkoll.where(:rfidnr => params[:student][:atr]).first
  end

  def api
    if params[:liu_id]
      @student = Student.where(:email => "#{params[:liu_id].downcase}@student.liu.se").first
    elsif params[:email]
      @student = Student.where(:email => params[:email].downcase).first
    elsif params[:rfid_number]
      @student = Student.where(:rfid_number => params[:rfid_number]).first
    elsif params[:barcode_number]
      @student = Student.where(:barcode_number => params[:barcode_number]).first
    elsif params[:personal_number]
      @student = Student.where(:personal_number => params[:personal_number]).first
    end

    if @student
      respond_to do |format|
        format.json { render :json => @student.to_json }
        format.xml  { render :xml => @student.to_xml }
      end
    else
      render :text => nil, :status => 404
    end
  end

private
  def verify_api_key
    authenticate_or_request_with_http_basic do |id, api_key|
      User.verify_api_key(id, api_key)
    end
  end
end
