import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'
import reportWebVitals from './reportWebVitals'
import '@fontsource/roboto'
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom"
import {Box} from "@material-ui/core"
import * as Sentry from "@sentry/react"
import { Integrations } from "@sentry/tracing"
import { LicenseInfo } from "@mui/x-data-grid-pro"
import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider
} from "@apollo/client";
import CapacityAndQueue from "./components/CapacityAndQueue"
import ChangeRequestDetail from "./components/ChangeRequestDetail"
import CompanyDetail from "./components/CompanyDetail"
import DedicatedTeamDetail from "./components/DedicatedTeamDetail"
import DedicatedTeamPlanningPeriodDetail from "./components/DedicatedTeamPlanningPeriodDetail"
import DedicatedTeamPlanningPeriodSystemDetail from "./components/DedicatedTeamPlanningPeriodSystemDetail"
import DedicatedTeamQuarterDetail from "./components/DedicatedTeamQuarterDetail"
import PlanningPeriodDetail from "./components/PlanningPeriodDetail"
import EpicDetail from "./components/EpicDetail"
import EpicSystemDetail from "./components/EpicSystemDetail"
import PersonDetail from "./components/PersonDetail"
import PersonList from "./components/PersonList"
import PersonListByProjectTeamIdAndMonth from "./components/PersonListByProjectTeamIdAndMonth"
import PersonMonthByPersonKeyAndMonth from "./components/PersonMonthDetailByPersonKeyAndMonth"
import PersonSystemChangeRequestDetail from "./components/PersonSystemChangeRequestDetail"
import PlanningPeriodPersonDetail from "./components/PlanningPeriodPersonDetail"
import PlanningPeriodPersonsList from "./components/PlanningPeriodPersonsList"
import PlanningPeriodProjectTeamsList from "./components/PlanningPeriodProjectTeamsList"
import ProjectManagerDetail from "./components/ProjectManagerDetail";
import ProjectManagerList from "./components/ProjectManagerList";
import ProjectTeamDetail from "./components/ProjectTeamDetail"
import ProjectTeamList from "./components/ProjectTeamList"
import ProjectTeamPlanningPeriodDetail from "./components/ProjectTeamPlanningPeriodDetail"
import ProjectTeamPlanningPeriodSystemDetail from "./components/ProjectTeamPlanningPeriodSystemDetail"
import ProjectTeamQuarterDetail from "./components/ProjectTeamQuarterDetail"
import SystemChangeRequestDetail from "./components/SystemChangeRequestDetail"
import SystemDetail from "./components/SystemDetail"
import SystemList from "./components/SystemList"
import SystemPlanningPeriodDetail from "./components/SystemPlanningPeriodDetail"
import QuarterDetail from "./components/QuarterDetail"
import QuarterProjectTeamList from "./components/QuarterProjectTeamList"

Sentry.init({
  dsn: "https://2bdd473a8cea45a495242e7259b2846d@o498438.ingest.sentry.io/5916644",
  integrations: [new Integrations.BrowserTracing()],

  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 0.01,
});

LicenseInfo.setLicenseKey('c96f4e151cafeb69315727049b583000T1JERVI6Mjk0NjAsRVhQSVJZPTE2NjMzMjQyODcwMDAsS0VZVkVSU0lPTj0x')

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
                        <Route exact path="/" component={ CompanyDetail } />
                        <Route exact path="/capacityAndQueue" component={ CapacityAndQueue } />
                        <Route exact path="/planningPeriods/:planningPeriodId/persons/" component={ PlanningPeriodPersonsList } />
                        <Route exact path="/planningPeriods/:planningPeriodId/projectTeams/" component={ PlanningPeriodProjectTeamsList } />
                        <Route exact path="/projectTeams/" component={ ProjectTeamList } />
                        <Route exact path="/systems/" component={ SystemList } />
                        <Route path="/dedicatedTeams/:dedicatedTeamId" component={ DedicatedTeamDetail } />
                        <Route path="/persons/:personKey/month/:month" component={ PersonMonthByPersonKeyAndMonth } />
                        <Route path="/persons/:key" component={ PersonDetail } />
                        <Route path="/projectManagers/:id" component={ ProjectManagerDetail } />
                        <Route path="/projectManagers/" component={ ProjectManagerList } />
                        <Route path="/projectTeams/:projectTeamId/month/:month/persons" component={ PersonListByProjectTeamIdAndMonth } />
                        <Route path="/projectTeams/:projectTeamId" component={ ProjectTeamDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/dedicatedTeams/:dedicatedTeamId/systems/:systemId" component={ DedicatedTeamPlanningPeriodSystemDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/dedicatedTeams/:dedicatedTeamId" component={ DedicatedTeamPlanningPeriodDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/projectTeams/:projectTeamId/systems/:systemId" component={ ProjectTeamPlanningPeriodSystemDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/projectTeams/:projectTeamId" component={ ProjectTeamPlanningPeriodDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/systems/:systemId" component={ SystemPlanningPeriodDetail } />
                        <Route path="/planningPeriods/:planningPeriodId/persons/:personKey" component={ PlanningPeriodPersonDetail } />
                        <Route path="/planningPeriods/:id" component={ PlanningPeriodDetail } />
                        <Route path="/systems/:systemId" component={ SystemDetail } />
                        <Route path="/quarters/:quarterKey/dedicatedTeams/:dedicatedTeamId" component={ DedicatedTeamQuarterDetail } />
                        <Route exact path="/quarters/:quarterKey/projectTeams/" component={ QuarterProjectTeamList } />
                        <Route path="/quarters/:quarterKey/projectTeams/:projectTeamId" component={ ProjectTeamQuarterDetail } />
                        <Route path="/quarters/:key" component={ QuarterDetail } />
                        <Route path="/epics/:epicKey/systems/:systemId" component={ EpicSystemDetail } />
                        <Route path="/epics/:key" component={ EpicDetail } />
                        <Route path="/changeRequests/:key" component={ ChangeRequestDetail } />
                        <Route path="/systemChangeRequests/:systemChangeRequestKey/persons/:personKey" component={ PersonSystemChangeRequestDetail } />
                        <Route path="/systemChangeRequests/:key" component={ SystemChangeRequestDetail } />
                        <Route path="/persons" component={ PersonList } />
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
