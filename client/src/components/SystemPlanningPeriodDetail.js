import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"

const fetchSystemPlanningPeriodByPlanningPeriodIdAndSystemId = gql`
    query SystemPlanningPeriodByPlanningPeriodIdAndSystemId($planningPeriodId: Int!, $systemId: Int!) {
          systemPlanningPeriodByPlanningPeriodIdAndSystemId(systemId: $systemId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                effortPerFunctionPoint
                system {
                    name
                }
                planningPeriod {
                    name
                    start
                    end
                }

                timeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                timeSpentCumsumAtEndPrediction
                
                systemChangeRequests {
                    id
                    estimate
                    timeLeft
                    hasValue
                    name
                    stateCategory {
                        id
                    }
                }
          }
    }
`;

class SystemPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }
        const planningPeriodId = this.props.match.params.planningPeriodId

        const systemPlanningPeriod = this.props.data.systemPlanningPeriodByPlanningPeriodIdAndSystemId

        const systemName = systemPlanningPeriod.system.name
        const estimate = systemPlanningPeriod.estimate
        const effortPerFunctionPoint = systemPlanningPeriod.effortPerFunctionPoint
        const planningPeriodName = systemPlanningPeriod.planningPeriod.name
        const planningPeriodStart = systemPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = systemPlanningPeriod.planningPeriod.end
        const projectTeams = systemPlanningPeriod.projectTeams
        const systemChangeRequests = systemPlanningPeriod.systemChangeRequests

        const timeSheetsByDate = systemPlanningPeriod.timeSheetsByDate
        const timeSpentCumsumAtEndPrediction = systemPlanningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Система { systemName }
                    <br />
                    Период планирования { planningPeriodName } ({ planningPeriodStart }-{ planningPeriodEnd })
                    <br />
                    Затраты на функциональную точку (аналитика + разработка + менеджмент) { effortPerFunctionPoint.toFixed(2) } часов / функциональная точка
                </Typography>

                <TimeSheetsByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Аналитика + Разработка + Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                    timeSpentCumsumAtEndPrediction={ timeSpentCumsumAtEndPrediction }
                />

                <Typography variant="body" noWrap>
                    Заявки на доработку
                </Typography>
                <ul>
                    { systemChangeRequests
                        .slice()
.                       sort(function(a, b) {
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
                            <li key={ systemChangeRequest.id }>
                                { systemChangeRequest.stateCategory.id !== 3 ? `Осталось ${ Math.round(systemChangeRequest.timeLeft) } ч ` : '' }
                                { systemChangeRequest.estimate === 0 && systemChangeRequest.stateCategory.id !== 3 ? `Оценка ${ Math.round(systemChangeRequest.estimate) } ч ` : '' }
                                { systemChangeRequest.hasValue ? '' : 'Нет ценности ' }

                                <RouterLink style={{ textDecoration: systemChangeRequest.stateCategory.id === 3 ? 'line-through' : 'none' }} to={ `/systemChangeRequests/${systemChangeRequest.id}` }>
                                    { systemChangeRequest.id } &nbsp;
                                    { systemChangeRequest.name }
                                </RouterLink>
                            </li>
                        )
                    )}
                 </ul>
            </Box>
        );
    }
}

export default graphql(fetchSystemPlanningPeriodByPlanningPeriodIdAndSystemId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, systemId: props.match.params.systemId }}}
})(SystemPlanningPeriodDetail);