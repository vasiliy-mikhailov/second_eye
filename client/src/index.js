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
import DedicatedTeamInPlanningPeriodDetail from "./components/DedicatedTeamPlanningPeriodDetail"
import ChangeRequestDetail from "./components/ChangeRequestDetail";
import SystemChangeRequestDetail from "./components/SystemChangeRequestDetail";
import {Box} from "@material-ui/core";

import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider
} from "@apollo/client";


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
                        <Route path="/planningPeriods/:planningPeriodId/dedicatedTeams/:dedicatedTeamId" component={ DedicatedTeamInPlanningPeriodDetail } />
                        <Route path="/planningPeriods/:id" component={ PlanningPeriodDetail } />
                        <Route path="/changeRequests/:id" component={ ChangeRequestDetail } />
                        <Route path="/systemChangeRequests/:id" component={ SystemChangeRequestDetail } />
                        <Route path="/" component={App} />
                    </Switch>
                </Router>
            </Box>
        </ApolloProvider>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
