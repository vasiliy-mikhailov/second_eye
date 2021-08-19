import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {CartesianGrid, Legend, ReferenceLine, Scatter, ScatterChart, XAxis, YAxis, ZAxis} from "recharts";
import moment from "moment";

const fetchDedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId = gql`
    query DedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId($planningPeriodId: String!, $dedicatedTeamId: String!) {
          dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId(dedicatedTeamId: $dedicatedTeamId, planningPeriodId: $planningPeriodId) {
                id
                estimate
                dedicatedTeam {
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

class DedicatedTeamPlanningPeriodDetail extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const dedicatedTeamPlanningPeriod = this.props.data.dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId
        const dedicatedTeamName = dedicatedTeamPlanningPeriod.dedicatedTeam.name
        const estimate = dedicatedTeamPlanningPeriod.estimate
        const planningPeriodName = dedicatedTeamPlanningPeriod.planningPeriod.name
        const planningPeriodStart = dedicatedTeamPlanningPeriod.planningPeriod.start
        const planningPeriodEnd = dedicatedTeamPlanningPeriod.planningPeriod.end
        const changeRequests = dedicatedTeamPlanningPeriod.changeRequests

        const timeSheetsByDate = dedicatedTeamPlanningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = dedicatedTeamPlanningPeriod.timeSpentPercentWithValueAndWithoutValueByDate

        const today = (new Date()).getTime()
        const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
        const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

        const allEdgeDates = [today, planningPeriodStart, planningPeriodEnd]

        if (firstTimeSheetDate) {
            allEdgeDates.push(firstTimeSheetDate)
        }

        if (lastTimeSheetDate) {
            allEdgeDates.push(lastTimeSheetDate)
        }

        const xAxisStart = Math.min(...allEdgeDates)
        const xAxisEnd = Math.max(...allEdgeDates)

        return (
            <Box>
                <Typography variant="body" noWrap>
                    Выделенная команда { dedicatedTeamName }
                    <br />
                    Период планирования { planningPeriodName } ({ planningPeriodStart }-{ planningPeriodEnd })
                </Typography>

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
                        domain={[xAxisStart - 1000 * 60 * 60 * 24 * 28, xAxisEnd + 1000 * 60 * 60 * 24 * 28]}
                        allowDataOverflow={true}
                        tickFormatter={(date) => moment(date).format('YYYY-MM-DD')}
                    />
                    <YAxis
                        type="number"
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>


                    <ReferenceLine x={ new Date(planningPeriodStart).getTime() } stroke="green" strokeDasharray="5 5" label="Начало периода" ifOverflow="extendDomain"/>

                    <ReferenceLine x={ new Date(planningPeriodEnd).getTime() } stroke="red" strokeDasharray="5 5" label="Окончание периода" ifOverflow="extendDomain"/>

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={ estimate } stroke="black" strokeDasharray="5 5" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано всего"
                        data= {
                            timeSheetsByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentCumsum: item.timeSpentCumsum }
                            })
                        }
                        line fill="black"
                    />
                </ScatterChart>
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
                        domain={[xAxisStart - 1000 * 60 * 60 * 24 * 28, xAxisEnd + 1000 * 60 * 60 * 24 * 28]}
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


                    <ReferenceLine x={ new Date(planningPeriodStart).getTime() } stroke="green" strokeDasharray="5 5" label="Начало периода" ifOverflow="extendDomain"/>

                    <ReferenceLine x={ new Date(planningPeriodEnd).getTime() } stroke="red" strokeDasharray="5 5" label="Окончание периода" ifOverflow="extendDomain"/>

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

export default graphql(fetchDedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId, {
    options: (props) => { return { variables: { planningPeriodId: props.match.params.planningPeriodId, dedicatedTeamId: props.match.params.dedicatedTeamId }}}
})(DedicatedTeamPlanningPeriodDetail);