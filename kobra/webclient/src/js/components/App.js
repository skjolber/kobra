import React from 'react'
import {Col, Grid, Navbar, Row, Well} from 'react-bootstrap'
import {connect} from 'react-redux'

import {LogInForm, MainFooter, MainNav, Page} from './'
import {isLoggedIn} from '../selectors'

const mapStateToProps = (state) => ({
  isLoggedIn: isLoggedIn(state)
})

const App = connect(mapStateToProps)((props) => (
  <div>
    <MainNav />
    {props.isLoggedIn ? (
      props.children
    ) : (
      <Page title="Log in">
        <Row>
          <Col sm={6}>
            <p className="lead">
              Kobra is a tool for looking up union and section membership of LiU
              students and for registrering union discounts.
            </p>
            <p>
              Access to Kobra is granted by the student union office.
            </p>
          </Col>
          <Col sm={6}>
            <LogInForm />
          </Col>
        </Row>
      </Page>
    )}
    <Grid>
      <MainFooter />
    </Grid>
  </div>
))

export {App}
