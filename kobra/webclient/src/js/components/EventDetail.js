import React from 'react'
import {Col, ControlLabel, FormControl, FormGroup, HelpBlock, Row, Table} from 'react-bootstrap'
import FontAwesome from 'react-fontawesome'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'

import {Page} from './'
import * as actions from '../actions'
import * as selectors from '../selectors'


const mapStateToProps = (state, {params}) => ({
  discounts: selectors.getAllDiscounts(state),
  event: selectors.getEventWithId(state, params.eventId),
  getTicketTypes: (eventUrl) => selectors.getEventTicketTypes(state, eventUrl),
  unions: selectors.getAllUnions(state)
})

const mapDispatchToProps = (dispatch) => ({
  handleNameChange: (eventUrl) => (domEvent) => dispatch(),
  handleSave: (domEvent) => dispatch()
})

const EventDetail = withRouter(connect(mapStateToProps, mapDispatchToProps)((props) => (
  props.event ? (
    <Page title={!!props.event ? props.event.get('name') : ''}>
      <p><a href=""><FontAwesome fixedWidth name="list"/> All organizations and events</a> </p>

      <Row>
        <Col sm={6}>
          <form onSubmit={props.handleSave}>
            <FormGroup>
              <ControlLabel>Name</ControlLabel>
              <FormControl type="text" placeholder="Name" onChange={props.handleNameChange()} />
            </FormGroup>
            <FormGroup>
              <ControlLabel>Ticket types</ControlLabel>
              <Table striped>
                <thead>
                  <tr>
                    <th>Name</th>
                    {props.unions.toKeyedSeq().map((union) => (
                      <th>{union.get('name')} discount</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {props.getTicketTypes(props.event.get('url')).toKeyedSeq().map((ticketType) => (
                    <tr>
                      <td>
                        <FormControl type="text" value={ticketType.get('name')}/>
                      </td>
                      {props.unions.toKeyedSeq().map((union) => {
                        const discount = props.discounts.find((d) => (
                          d.get('ticketType') === ticketType.get('url') && d.get('union') === union.get('url')
                        ))

                        return (
                          <td>
                            <FormControl type="number" value={discount.get('amount')} />
                          </td>
                        )
                      })}
                    </tr>
                  ))}
                </tbody>
              </Table>
            </FormGroup>
          </form>
        </Col>
        <Col sm={6}>

        </Col>
      </Row>
    </Page>
  ) : (
    <div/>
  )
)))

export {EventDetail}
