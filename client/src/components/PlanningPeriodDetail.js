import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"
import ValueByDatePeriodChart from "./ValueByDatePeriodChart"

const fetchPlanningPeriodById = gql`
    query PlanningPeriodByIdQuery($id: Int!) {
        planningPeriodById(id: $id) {
            id 
            name
            start
            end
            estimate
            
            dedicatedTeams {
                id
                name
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
                
                stateCategoryId
            }
        }
    }
`;

class PlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const planningPeriodId = this.props.match.params.id
        const planningPeriod = this.props.data.planningPeriodById
        const estimate = planningPeriod.estimate
        const planningPeriodStart = planningPeriod.start
        const planningPeriodEnd = planningPeriod.end

        const dedicatedTeams = planningPeriod.dedicatedTeams
        const changeRequests = planningPeriod.changeRequests

        const timeSheetsByDate = planningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = planningPeriod.timeSpentPercentWithValueAndWithoutValueByDate
        const timeSpentCumsumAtEndPrediction = planningPeriod.timeSpentCumsumAtEndPrediction

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        return (
            <Box>
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

                <Typography variant="body1" noWrap>
                    Выделенные команды
                </Typography>

               <ul>
                    { dedicatedTeams
                        .slice()
                        .sort(function(a, b) {
                            if (a.name > b.name) {
                                return 1;
                            }
                            if (a.name === b.name) {
                                return 0;
                            }
                            if (a.name < b.name) {
                                return -1;
                            }
                        })
                        .map(dedicatedTeam => (
                            <li key={ dedicatedTeam.id }>
                                <RouterLink to={ `/planningPeriods/${planningPeriodId}/dedicatedTeams/${dedicatedTeam.id}` }>
                                { dedicatedTeam.name }
                                </RouterLink>
                            </li>
                        )
                    )}
                </ul>

                <Typography variant="body1" noWrap>
                    Заявки на доработку
                </Typography>
               <ul>
                    { changeRequests
                        .slice()
.                       sort(function(a, b) {
                            if (a.stateCategoryId === 3 && b.stateCategoryId !== 3) {
                                return 1;
                            }
                            if (a.stateCategoryId === 3 && b.stateCategoryId === 3) {
                                return 0;
                            }
                            if (a.stateCategoryId !== 3 && b.stateCategoryId === 3) {
                                return -1;
                            }

                            return b.timeLeft - a.timeLeft
                        })
                        .map(changeRequest => (
                            <li key={ changeRequest.id }>
                                { changeRequest.stateCategoryId !== 3 ? `Осталось ${ Math.round(changeRequest.timeLeft) } ч ` : '' }
                                { changeRequest.estimate === 0 && changeRequest.stateCategoryId !== 3 ? `Оценка ${ Math.round(changeRequest.estimate) } ч ` : '' }
                                { changeRequest.hasValue ? '' : 'Нет ценности ' }

                                <RouterLink style={{ textDecoration: changeRequest.stateCategoryId === 3 ? 'line-through' : 'none' }} to={ `/changeRequests/${changeRequest.id}` }>
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

export default graphql(fetchPlanningPeriodById, {
    options: (props) => { return { variables: { id: props.match.params.id }}}
})(PlanningPeriodDetail);