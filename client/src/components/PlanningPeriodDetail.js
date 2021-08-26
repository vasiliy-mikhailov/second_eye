import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {CartesianGrid, Legend, ReferenceLine, Scatter, ScatterChart, XAxis, YAxis, ZAxis} from "recharts";
import moment from "moment";
import TimeSheetsByDatePeriodChart from "./TimeSheetsByDatePeriodChart"

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
            }
            
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
        const planningPeriodName = planningPeriod.name
        const planningPeriodStart = planningPeriod.start
        const planningPeriodEnd = planningPeriod.end

        const dedicatedTeams = planningPeriod.dedicatedTeams
        const changeRequests = planningPeriod.changeRequests

        const timeSheetsByDate = planningPeriod.timeSheetsByDate
        const timeSpentPercentWithValueAndWithoutValueByDate = planningPeriod.timeSpentPercentWithValueAndWithoutValueByDate

        const today = (new Date()).getTime()
        const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
        const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

        const xAxisStart = new Date(planningPeriodStart).getTime()
        const xAxisEnd = new Date(planningPeriodEnd).getTime()

        return (
            <Box>
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
                        domain={ [dataMin => xAxisStart, dataMax => xAxisEnd] }
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