import React from 'react'
import {Alert, Button, ControlLabel, FormControl, FormGroup} from 'react-bootstrap'
import {connect} from 'react-redux'

import {logIn, setEmail, setPassword} from '../actions'
import * as selectors from '../selectors'

const mapStateToProps = (state) => ({
  email: selectors.getEmail(state),
  password: selectors.getPassword(state),
  isPending: selectors.logInIsPending(state),
  logInError: selectors.getLogInError(state)
})

const mapDispatchToProps = (dispatch) => ({
  handleEmailChange: (domEvent) => {
    dispatch(setEmail(domEvent.target.value))
  },
  handlePasswordChange: (domEvent) => {
    dispatch(setPassword(domEvent.target.value))
  },
  handleSubmit: (domEvent) => {
    dispatch(logIn())
    domEvent.preventDefault()
  }
})

const LogInForm = connect(mapStateToProps, mapDispatchToProps)((props) => (
  <form onSubmit={props.handleSubmit}>
    <FormGroup bsSize="lg">
      <ControlLabel>Email address</ControlLabel>
      <FormControl type="email" placeholder="Email address" value={props.email}
                   onChange={props.handleEmailChange} />
      <FormControl.Feedback />
    </FormGroup>
    <FormGroup bsSize="lg">
      <ControlLabel>Password</ControlLabel>
      <FormControl type="password" placeholder="Password" value={props.password}
                   onChange={props.handlePasswordChange} />
      <FormControl.Feedback />
    </FormGroup>
    <FormGroup>
      <Button type="submit" block bsStyle="primary" bsSize="lg"
              disabled={props.isPending}>
        {props.isPending ? (
          <span>Logging in...</span>
        ) : (
          <span>Log in</span>
        )}
      </Button>
    </FormGroup>
    {!props.logInError ? (
      <div />
    ) : (
      <Alert bsStyle="danger">
        {props.logInError.message}
      </Alert>
    )}
  </form>
))

export {LogInForm}
