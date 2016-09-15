import React from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router'

import {Page} from './'
import * as actions from '../actions'
import * as selectors from '../selectors'

const mapStateToProps = (state, {params}) => ({
  organization: selectors.getOrganizationWithId(params.organizationId)
})

const mapDispatchToProps = (dispatch) => ({

})

const OrganizationDetail = withRouter(connect(mapStateToProps, mapDispatchToProps)((props) => (
  <Page>

  </Page>
)))

export {OrganizationDetail}
