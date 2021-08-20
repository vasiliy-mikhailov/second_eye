import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import '@fontsource/roboto';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import PlanningPeriodsList from "./components/PlanningPeriodsList";
import PlanningPeriodDetail from "./components/PlanningPeriodDetail";
import DedicatedTeamPlanningPeriodDetail from "./components/DedicatedTeamPlanningPeriodDetail"
import ProjectTeamPlanningPeriodDetail from "./components/ProjectTeamPlanningPeriodDetail"
import ChangeRequestDetail from "./components/ChangeRequestDetail";
import SystemChangeRequestDetail from "./components/SystemChangeRequestDetail";
import {Box} from "@material-ui/core";
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";

import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider
} from "@apollo/client";

Sentry.init({
  dsn: "https://2bdd473a8cea45a495242e7259b2846d@o498438.ingest.sentry.io/5916644",
  integrations: [new Integrations.BrowserTracing()],

  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 0.01,
});

const client = new ApolloClient({
    uri: process.env.REACT_APP_SECOND_EYE_API_URL,
    cache: new InMemoryCache()
});

ReactDOM.render(
    <React.StrictMode>
        <ApolloProvider client={client}>
            <Box m="1rem">
                <Router>
                    <Switch>
                        {/*<Route exact path="/" >*/}
                        {/*    <Redirect to="/planningPeriods/2021" />*/}
                        {/*</Route>*/}
                        <Route exact path="/" component={ PlanningPeriodsList } />
                        <Route exact path="/planningPeriods" component={ PlanningPeriodsList } />
                        <Route path="/planningPeriods/:planningPeriodId/dedicatedTeams/:dedicatedTeamId" component={ DedicatedTeamPlanningPeriodDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/projectTeams/:projectTeamId" component={ ProjectTeamPlanningPeriodDetail } />
                        <Route path="/planningPeriods/:id" component={ PlanningPeriodDetail } />
                        <Route path="/changeRequests/:id" component={ ChangeRequestDetail } />
                        <Route path="/systemChangeRequests/:id" component={ SystemChangeRequestDetail } />
                        <Route path="/" component={App} />
                    </Switch>
                </Router>
            </Box>
        </ApolloProvider>
    </React.StrictMode>
    ,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
