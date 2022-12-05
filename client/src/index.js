import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'
import reportWebVitals from './reportWebVitals'
import '@fontsource/roboto'
import {
    BrowserRouter as Router,
    Routes,
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

LicenseInfo.setLicenseKey('29d15176019c4254d109b514e026d8f8Tz01MzkxNCxFPTE2OTk0NjkxNTIxODksUz1wcm8sTE09cGVycGV0dWFsLEtWPTI=')

const client = new ApolloClient({
    uri: process.env.REACT_APP_SECOND_EYE_API_URL,
    cache: new InMemoryCache()
});

ReactDOM.render(
    <React.StrictMode>
        <ApolloProvider client={client}>
            <Box m="1rem">
                <Router>
                    <Routes>
                        {/*<Route exact path="/" >*/}
                        {/*    <Redirect to="/planningPeriods/2021" />*/}
                        {/*</Route>*/}
                        <Route exact path="/" element={ <CompanyDetail /> } />
                        <Route exact path="/capacityAndQueue" element={ <CapacityAndQueue /> } />
                        <Route exact path="/planningPeriods/:planningPeriodId/persons/" element={ <PlanningPeriodPersonsList /> } />
                        <Route exact path="/planningPeriods/:planningPeriodId/projectTeams/" element={ <PlanningPeriodProjectTeamsList /> } />
                        <Route exact path="/projectTeams/" element={ <ProjectTeamList /> } />
                        <Route exact path="/systems/" element={ <SystemList /> } />
                        <Route path="/dedicatedTeams/:dedicatedTeamId" element={ <DedicatedTeamDetail /> } />
                        <Route path="/persons/:personKey/month/:month" element={ <PersonMonthByPersonKeyAndMonth /> } />
                        <Route path="/persons/:key" element={ <PersonDetail /> } />
                        <Route path="/projectManagers/:id" element={ <ProjectManagerDetail /> } />
                        <Route path="/projectManagers/" element={ <ProjectManagerList /> } />
                        <Route path="/projectTeams/:projectTeamId/month/:month/persons" element={ <PersonListByProjectTeamIdAndMonth />} />
                        <Route path="/projectTeams/:projectTeamId" element={ <ProjectTeamDetail /> } />
                        <Route path="/planningPeriods/:planningPeriodId/dedicatedTeams/:dedicatedTeamId/systems/:systemId" element={ <DedicatedTeamPlanningPeriodSystemDetail /> } />
                        <Route path="/planningPeriods/:planningPeriodId/dedicatedTeams/:dedicatedTeamId" element={ <DedicatedTeamPlanningPeriodDetail /> } />
                        <Route path="/planningPeriods/:planningPeriodId/projectTeams/:projectTeamId/systems/:systemId" element={ <ProjectTeamPlanningPeriodSystemDetail /> } />
                        <Route path="/planningPeriods/:planningPeriodId/projectTeams/:projectTeamId" element={ <ProjectTeamPlanningPeriodDetail /> } />
                        <Route path="/planningPeriods/:planningPeriodId/systems/:systemId" element={ <SystemPlanningPeriodDetail /> } />
                        <Route path="/planningPeriods/:planningPeriodId/persons/:personKey" element={ <PlanningPeriodPersonDetail /> } />
                        <Route path="/planningPeriods/:id" element={ <PlanningPeriodDetail /> } />
                        <Route path="/systems/:systemId" element={ <SystemDetail /> } />
                        <Route path="/quarters/:quarterKey/dedicatedTeams/:dedicatedTeamId" element={ <DedicatedTeamQuarterDetail /> } />
                        <Route exact path="/quarters/:quarterKey/projectTeams/" element={ <QuarterProjectTeamList /> } />
                        <Route path="/quarters/:quarterKey/projectTeams/:projectTeamId" element={ <ProjectTeamQuarterDetail /> } />
                        <Route path="/quarters/:key" element={ <QuarterDetail /> } />
                        <Route path="/epics/:epicKey/systems/:systemId" element={ <EpicSystemDetail /> } />
                        <Route path="/epics/:key" element={ <EpicDetail /> } />
                        <Route path="/changeRequests/:key" element={ <ChangeRequestDetail />} />
                        <Route path="/systemChangeRequests/:systemChangeRequestKey/persons/:personKey" element={ <PersonSystemChangeRequestDetail />} />
                        <Route path="/systemChangeRequests/:key" element={ <SystemChangeRequestDetail /> } />
                        <Route path="/persons" element={ <PersonList /> } />
                        <Route path="/" element={ <App /> } />
                    </Routes>
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
