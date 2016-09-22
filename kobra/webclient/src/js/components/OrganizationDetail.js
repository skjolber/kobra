import React from 'react'
import {Col, ControlLabel, FormControl, FormGroup, Row} from 'react-bootstrap'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'

import {Page} from './'
import * as actions from '../actions'
import * as selectors from '../selectors'

const mapStateToProps = (state, {params}) => ({
  organization: selectors.getOrganizationWithId(state, params.organizationId),
  users: selectors.getAllUsers(state)
})

const mapDispatchToProps = (dispatch) => ({
  handleAdminsChange: (organizationUrl) => (domEvent) => {
    const adminUrls = [...domEvent.target.options]
      .filter(o => o.selected)
      .map(o => o.value)

    return dispatch(actions.setOrganizationAdmins(organizationUrl, adminUrls))
  },
  handleNameChange: (organizationUrl) => (domEvent) => dispatch(
    actions.setOrganizationName(organizationUrl, domEvent.target.value)
  )
})

const OrganizationDetail = withRouter(connect(mapStateToProps, mapDispatchToProps)((props) => (
  <Page title="Manage organization">
    {props.organization ? (
      <form>
        <FormGroup>
          <ControlLabel>Name</ControlLabel>
          <FormControl type="text"
                       value={props.organization.getIn(['_changes', 'name'], props.organization.get('name'))}
                       onChange={props.handleNameChange(props.organization.get('url'))} />
        </FormGroup>
        <FormGroup>
          <ControlLabel>Administrators</ControlLabel>
          <FormControl componentClass="select" multiple
                       value={props.organization.getIn(['_changes', 'admins'],
                         props.organization.get('admins'))}
                       onChange={props.handleAdminsChange(
                         props.organization.get('url'))}>
            {props.users.toKeyedSeq().map((user) => (
              <option value={user.get('url')}>{user.get('name')} ({user.get('email')})</option>
            ))}
          </FormControl>
        </FormGroup>
      </form>
    ) : (
      <div />
    )}

  </Page>
)))

export {OrganizationDetail}
