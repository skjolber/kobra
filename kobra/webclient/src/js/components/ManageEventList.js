import React from 'react'
import {connect} from 'react-redux'

import * as selectors from '../selectors'

const mapStateToProps = (state) => ({
  events: selectors.getEvents(state),
  organization: selectors.getOrganizations(state)
})

const ManageEventList = connect(mapStateToProps)((props) => (
  <div>

  </div>
))

export {ManageEventList}
