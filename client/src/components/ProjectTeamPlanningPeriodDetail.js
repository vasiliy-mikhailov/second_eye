import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"

const fetchProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId = gql`
    query ProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId($planningPeriodId: Int!, $projectTeamId: Int!) {
          projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId(projectTeamId: $projectTeamId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                projectTeam {
                    name
                }
                planningPeriod {
                    name
                    start
                    end
                }
                timeSpentPercentWithValueAndWithoutValueByDate {
                    date
                    timeSpentWithoutValuePercentCumsum
                    timeSpentWithValuePercentCumsum
                }
                timeSheetsByDate {
                    date
                    timeSpentCumsum
                    timeSpentCumsumPrediction
                }
                
                timeSpentCumsumAtEndPrediction
                
                changeRequests {
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

class ProjectTeamPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const projectTeamPlanningPeriod = this.props.data.projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId
        const projectTeamName = projectTeamPlanningPeriod.projectTeam.name
        const estimate = projectTeamPlanningPeriod.estimate
        const planningPeriodName = projectTeamPlanningPeriod.planningPeriod.name
        const planningPeriodStart = projectTeamPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = projectTeamPlanningPeriod.planningPeriod.end
        const changeRequests = projectTeamPlanningPeriod.changeRequests

        const timeSheetsByDate = projectTeamPlanningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = projectTeamPlanningPeriod.timeSpentPercentWithValueAndWithoutValueByDate
        const timeSpentCumsumAtEndPrediction = projectTeamPlanningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Проектная команда { projectTeamName }
                    <br />
                    Период планирования { planningPeriodName } ({ planningPeriodStart }-{ planningPeriodEnd })
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

                <ValueByDatePeriodChart
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Доля списаний на задачи без бизнес-ценности"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSpentPercentWithValueAndWithoutValueByDate={ timeSpentPercentWithValueAndWithoutValueByDate }
                />

                <Typography variant="body" noWrap>
                    Заявки на доработку
                </Typography>
                <ul>
                    { changeRequests
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
                        .map(changeRequest => (
                            <li key={ changeRequest.id }>
                                { changeRequest.stateCategory.id !== 3 ? `Осталось ${ changeRequest.timeLeft } ч ` : '' }
                                { changeRequest.estimate === 0 && changeRequest.stateCategory.id !== 3 ? `Оценка ${ changeRequest.estimate } ч ` : '' }
                                { changeRequest.hasValue ? '' : 'Нет ценности ' }

                                <RouterLink style={{ textDecoration: changeRequest.stateCategory.id === 3 ? 'line-through' : 'none' }} to={ `/changeRequests/${changeRequest.id}` }>
                                    { changeRequest.id } &nbsp;
                                    { changeRequest.name }
                                </RouterLink>
                            </li>
                        )
                    )}
                 </ul>
            </Box>
        );
    }
}

export default graphql(fetchProjectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, projectTeamId: props.match.params.projectTeamId }}}
})(ProjectTeamPlanningPeriodDetail);