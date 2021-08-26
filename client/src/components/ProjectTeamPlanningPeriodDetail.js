import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {CartesianGrid, Legend, ReferenceLine, Scatter, ScatterChart, XAxis, YAxis, ZAxis} from "recharts";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"

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
                }
                
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

        const planningPeriodId = this.props.match.params.planningPeriodId

        const projectTeamPlanningPeriod = this.props.data.projectTeamPlanningPeriodByPlanningPeriodIdAndProjectTeamId
        console.log(projectTeamPlanningPeriod)
        const projectTeamName = projectTeamPlanningPeriod.projectTeam.name
        const estimate = projectTeamPlanningPeriod.estimate
        const planningPeriodName = projectTeamPlanningPeriod.planningPeriod.name
        const planningPeriodStart = projectTeamPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = projectTeamPlanningPeriod.planningPeriod.end
        const changeRequests = projectTeamPlanningPeriod.changeRequests

        const timeSheetsByDate = projectTeamPlanningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = projectTeamPlanningPeriod.timeSpentPercentWithValueAndWithoutValueByDate

        const today = (new Date()).getTime()
        const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
        const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

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
                    planningPeriodStart={ planningPeriodStart }
                    planningPeriodEnd={ planningPeriodEnd }
                    title="Аналитика + Разработка + Тестирование"
                    xAxisStart={ xAxisStart }
                    xAxisEnd={ xAxisEnd }
                    color="black"
                    timeSheetsByDate={ timeSheetsByDate }
                    estimate={ estimate }
                />

                <ScatterChart
                    width={1440}
                    height={200}
                    margin={{
                        left: -5,
                    }}
                >
                    <CartesianGrid />
                    <XAxis
                        dataKey="date"
                        type="number"
                        domain={[xAxisStart, xAxisEnd]}
                        allowDataOverflow={true}
                        tickFormatter={(date) => moment(date).format('YYYY-MM-DD')}
                    />
                    <YAxis
                        type="number"
                        dataKey="timeSpentWithoutValuePercentCumsum"
                        tickFormatter={(tick) => {
                            return `${ tick * 100 }%`;
                        }}
                    />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>


                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={ 1 } stroke="black" strokeDasharray="5 5" ifOverflow="extendDomain" />
                    <Scatter
                        name="Доля списаний на задачи без ценности"
                        data= {
                            timeSpentPercentWithValueAndWithoutValueByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentWithoutValuePercentCumsum: item.timeSpentWithoutValuePercentCumsum }
                            })
                        }
                        line fill="black"
                    />
                </ScatterChart>

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