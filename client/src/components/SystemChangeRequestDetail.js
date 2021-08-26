import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'

const fetchSystemChangeRequest = gql`
    query SystemChangeRequestByIdQuery($id: String!) {
        systemChangeRequestById(id: $id) {
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
            
            changeRequest {
                plannedInstallDate
            }
        }
    }
`;

class SystemChangeRequestDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const systemChangeRequest = this.props.data.systemChangeRequestById
        const changeRequest = systemChangeRequest.changeRequest
        const plannedInstallDate = changeRequest.plannedInstallDate ? new Date(changeRequest.plannedInstallDate).getTime() : null
        const timeSheetsByDate = systemChangeRequest.timeSheetsByDate
        const estimate = systemChangeRequest.estimate

        const analysisTimeSheetsByDate = systemChangeRequest.analysisTimeSheetsByDate
        const analysisEstimate = systemChangeRequest.analysisEstimate

        const developmentTimeSheetsByDate = systemChangeRequest.developmentTimeSheetsByDate
        const developmentEstimate = systemChangeRequest.developmentEstimate

        const testingTimeSheetsByDate = systemChangeRequest.testingTimeSheetsByDate
        const testingEstimate = systemChangeRequest.testingEstimate

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
                    <Link href={ this.props.location.pathname }>
                        { systemChangeRequest.id }
                    </Link> &nbsp;
                    { systemChangeRequest.name } &nbsp;
                    { systemChangeRequest.state.name } &nbsp;
                    <Link href={ systemChangeRequest.url }>
                        [ источник ]
                    </Link>
                    <br />
                    Осталось { Math.round(systemChangeRequest.timeLeft) } ч ( { (systemChangeRequest.timeLeft / systemChangeRequest.estimate * 100).toFixed(2) }% ) <br />
                    Сделано { Math.round(systemChangeRequest.timeSpent) } ч <br />
                    Оценка { Math.round(systemChangeRequest.estimate) } ч <br />
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
            </Box>
        );
    }
}

export default graphql(fetchSystemChangeRequest, {
    options: (props) => { return { variables: { id: props.match.params.id }}}
})(SystemChangeRequestDetail);