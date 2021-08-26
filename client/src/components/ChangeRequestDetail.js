import React, {Component} from "react";
import {gql} from '@apollo/client';
import {graphql} from '@apollo/client/react/hoc';
import moment from 'moment';
import Typography from '@material-ui/core/Typography';
import {Link as RouterLink, NavLink} from "react-router-dom"
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'

const fetchChangeRequest = gql`
    query ChangeRequestByIdQuery($id: String!) {
        changeRequestById(id: $id) {
            id 
            url
            name
            state {
                name
            }
            
            analysisEstimate
            analysisTimeSpent
            analysisTimeLeft
            analysisTimeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            developmentEstimate
            developmentTimeSpent
            developmentTimeLeft
            developmentTimeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            testingEstimate
            testingTimeSpent
            testingTimeLeft
            testingTimeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            estimate
            timeSpent
            timeLeft
            timeSheetsByDate {
                date
                timeSpentCumsum
            }
            
            plannedInstallDate
            
            systemChangeRequests {
                id
                name
                
                estimate
                timeLeft
                state {
                    name
                }
                stateCategory {
                    id
                }
            }
        }
    }
`;

class ChangeRequestDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const changeRequest = this.props.data.changeRequestById

        const plannedInstallDate = changeRequest.plannedInstallDate ? new Date(changeRequest.plannedInstallDate).getTime() : null
        const timeSheetsByDate = changeRequest.timeSheetsByDate
        const estimate = changeRequest.estimate

        const analysisTimeSheetsByDate = changeRequest.analysisTimeSheetsByDate
        const analysisEstimate = changeRequest.analysisEstimate

        const developmentTimeSheetsByDate = changeRequest.developmentTimeSheetsByDate
        const developmentEstimate = changeRequest.developmentEstimate

        const testingTimeSheetsByDate = changeRequest.testingTimeSheetsByDate
        const testingEstimate = changeRequest.testingEstimate

        const today = (new Date()).getTime()
        const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
        const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

        const allEdgeDates = [today]
        if (plannedInstallDate) {
            allEdgeDates.push(plannedInstallDate)
        }

        if (firstTimeSheetDate) {
            allEdgeDates.push(firstTimeSheetDate)
        }

        if (lastTimeSheetDate) {
            allEdgeDates.push(lastTimeSheetDate)
        }

        const xAxisStart = Math.min(...allEdgeDates) - 1000 * 60 * 60 * 24 * 28
        const xAxisEnd = Math.max(...allEdgeDates) + 1000 * 60 * 60 * 24 * 28

        return (
            <Box>
                <Typography variant="body1" noWrap>
                    <NavLink to={ this.props.location.pathname }>
                        { changeRequest.id }
                    </NavLink> &nbsp;
                    { changeRequest.name } &nbsp;
                    { changeRequest.state.name } &nbsp;
                    <Link href={ changeRequest.url }>
                        [ источник ]
                    </Link>
                    <br />
                    Осталось { Math.round(changeRequest.timeLeft) } ч ( { (changeRequest.timeLeft / changeRequest.estimate * 100).toFixed(2) }% ) <br />
                    Сделано { Math.round(changeRequest.timeSpent) } ч <br />
                    Оценка { Math.round(changeRequest.estimate) } ч <br />
                    Плановая дата установки { plannedInstallDate ? moment(plannedInstallDate).format("YYYY-MM-DD") : "не указана"} <br />
                </Typography>
                <br />
                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Аналитика + Разработка + Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Аналитика"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="red"
                    timeSheetsByDate={ analysisTimeSheetsByDate }
                    estimate={ analysisEstimate }
                />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Разработка"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="green"
                    timeSheetsByDate={ developmentTimeSheetsByDate }
                    estimate={ developmentEstimate }
                />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="blue"
                    timeSheetsByDate={ testingTimeSheetsByDate }
                    estimate={ testingEstimate }
                />

                <ul>
                    { changeRequest.systemChangeRequests
                        .slice()
                        .sort(function(a, b) {
                            if (a.stateCategory.id === 3 && b.stateCategory.id !== 3) {
                                return 1;
                            }
                            if (a.stateCategory.id === 3 && b.stateCategory.id === 3) {
                                return 0;
                            }
                            if (a.stateCategory.id !== 3 && b.stateCategory.id === 3) {
                                return -1;
                            }

                            return b.timeLeft - a.timeLeft
                        })
                        .map(systemChangeRequest => (
                            <li key={systemChangeRequest.id}>
                                { systemChangeRequest.stateCategory.id !== 3 ? `Осталось ${ Math.round(systemChangeRequest.timeLeft) } ч ` : '' }
                                { systemChangeRequest.estimate === 0 && systemChangeRequest.stateCategory.id !== 3 ? `Оценка ${ Math.round(systemChangeRequest.estimate) } ч ` : '' }

                                <RouterLink style={{ textDecoration: systemChangeRequest.stateCategory.id === 3 ? 'line-through' : 'none' }} to={ `/systemChangeRequests/${systemChangeRequest.id}` }>
                                    {systemChangeRequest.name}
                                </RouterLink>
                            </li>
                        )
                    )}
                </ul>
            </Box>
        );
    }
}

export default graphql(fetchChangeRequest, {
    options: (props) => { return { variables: { id: props.match.params.id }}}
})(ChangeRequestDetail);