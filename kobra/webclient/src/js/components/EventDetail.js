import React from 'react'
import {Breadcrumb} from 'react-bootstrap'
import FontAwesome from 'react-fontawesome'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'

import {Page} from './'
import * as selectors from '../selectors'


const mapStateToProps = (state, {params}) => ({
  event: selectors.getEventWithId(state, params.eventId),
})

const EventDetail = withRouter(connect(mapStateToProps)((props) => (
  <Page title={!!props.event ? props.event.get('name') : ''}>
    <p><a href=""><FontAwesome fixedWidth name="list"/> Back to all organizations and events</a> </p>

    hej
  </Page>
)))

export {EventDetail}
