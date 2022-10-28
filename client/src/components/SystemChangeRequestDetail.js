import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import TimeSheetsByDateIssueChart from './TimeSheetsByDateIssueChart'

const fetchSystemChangeRequestByKey = gql`
    query SystemChangeRequestByKeyQuery($key: String!) {
        systemChangeRequestByKey(key: $key) {
            id
            key
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
            effortPerFunctionPoint
            timeSpent
            timeLeft
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
            }
            
            calculatedFinishDate
            
            changeRequest {
                plannedInstallDate
            }
        }
    }
`;

class SystemChangeRequestDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const systemChangeRequestKey = this.props.match.params.key
        const systemChangeRequest = this.props.data.systemChangeRequestByKey
        const changeRequest = systemChangeRequest.changeRequest
        const plannedInstallDate = changeRequest.plannedInstallDate ? new Date(changeRequest.plannedInstallDate).getTime() : null
        const timeSheetsByDate = systemChangeRequest.timeSheetsByDate
        const estimate = systemChangeRequest.estimate
        const effortPerFunctionPoint = systemChangeRequest.effortPerFunctionPoint

        const analysisTimeSheetsByDate = systemChangeRequest.analysisTimeSheetsByDate
        const analysisEstimate = systemChangeRequest.analysisEstimate

        const developmentTimeSheetsByDate = systemChangeRequest.developmentTimeSheetsByDate
        const developmentEstimate = systemChangeRequest.developmentEstimate

        const testingTimeSheetsByDate = systemChangeRequest.testingTimeSheetsByDate
        const testingEstimate = systemChangeRequest.testingEstimate

        const calculatedFinishDate = systemChangeRequest.calculatedFinishDate

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

        if (calculatedFinishDate) {
            allEdgeDates.push(new Date(calculatedFinishDate).getTime())
        }

        const xAxisStart = Math.min(...allEdgeDates) - 1000 * 60 * 60 * 24 * 28
        const xAxisEnd = Math.max(...allEdgeDates) + 1000 * 60 * 60 * 24 * 28

        return (
            <Box>
                <Typography variant="body1" noWrap>
                    <Link href={ this.props.location.pathname } target="_blank">
                        { systemChangeRequestKey }
                    </Link> &nbsp;
                    { systemChangeRequest.name } &nbsp;
                    { systemChangeRequest.state.name } &nbsp;
                    <Link href={ systemChangeRequest.url }>
                        [ источник ]
                    </Link>
                    <br />
                    Осталось { systemChangeRequest.timeLeft.toFixed(1) } ч ( { (systemChangeRequest.timeLeft / systemChangeRequest.estimate * 100).toFixed(2) }% ) <br />
                    Сделано { systemChangeRequest.timeSpent.toFixed(1) } ч <br />
                    Оценка { systemChangeRequest.estimate.toFixed(1) } ч <br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка
                </Typography>
                <br />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Аналитика"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="red"
                    timeSheetsByDate={ analysisTimeSheetsByDate }
                    estimate={ analysisEstimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Разработка"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="green"
                    timeSheetsByDate={ developmentTimeSheetsByDate }
                    estimate={ developmentEstimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />

                <TimeSheetsByDateIssueChart
                    plannedInstallDate={ plannedInstallDate }
                    title="Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="blue"
                    timeSheetsByDate={ testingTimeSheetsByDate }
                    estimate={ testingEstimate }
                    calculatedFinishDate={ calculatedFinishDate }
                />
            </Box>
        );
    }
}

export default graphql(fetchSystemChangeRequestByKey, {
    options: (props) => { return { variables: { key: props.match.params.key }}}
})(SystemChangeRequestDetail);