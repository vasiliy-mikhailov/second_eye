import React, {Component} from "react";
import {
    ScatterChart,
    CartesianGrid,
    Legend,
    XAxis,
    YAxis,
    ReferenceLine,
    ZAxis, Scatter
} from "recharts";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import moment from 'moment';
import Typography from '@material-ui/core/Typography';
import { Link as RouterLink, NavLink } from "react-router-dom"
import { Box, Link } from "@material-ui/core";


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

        const plannedInstallDate = this.props.data.changeRequestById.plannedInstallDate ? new Date(this.props.data.changeRequestById.plannedInstallDate).getTime() : null
        const timeSheetsByDate = this.props.data.changeRequestById.timeSheetsByDate

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

        const xAxisStart = Math.min(...allEdgeDates)
        const xAxisEnd = Math.max(...allEdgeDates)

        return (
            <Box>
                <Typography variant="body1" noWrap>
                    <NavLink to={ this.props.location.pathname }>
                        { this.props.data.changeRequestById.id }
                    </NavLink> &nbsp;
                    { this.props.data.changeRequestById.name } &nbsp;
                    { this.props.data.changeRequestById.state.name } &nbsp;
                    <Link href={ this.props.data.changeRequestById.url }>
                        [ источник ]
                    </Link>
                    <br />
                    Осталось { this.props.data.changeRequestById.timeLeft } ч ( { (this.props.data.changeRequestById.timeLeft / this.props.data.changeRequestById.estimate * 100).toFixed(2) }% ) <br />
                    Сделано { this.props.data.changeRequestById.timeSpent } ч <br />
                    Оценка { this.props.data.changeRequestById.estimate } ч <br />
                    Плановая дата установки { plannedInstallDate ? moment(plannedInstallDate).format("YYYY-MM-DD") : "не указана"} <br />
                </Typography>
                <br />

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
                    <YAxis type="number" dataKey="timeSpentCumsum" />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>

                    {
                        (this.props.data.changeRequestById.plannedInstallDate) ?
                            <ReferenceLine x={ new Date(this.props.data.changeRequestById.plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={ this.props.data.changeRequestById.estimate } stroke="black" strokeDasharray="5 5" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано всего"
                        data= {
                            this.props.data.changeRequestById.timeSheetsByDate.map(item => {
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
                    <YAxis type="number" dataKey="timeSpentCumsum" />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>
                    {
                        (this.props.data.changeRequestById.plannedInstallDate) ?
                            <ReferenceLine x={ new Date(this.props.data.changeRequestById.plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.changeRequestById.analysisEstimate} stroke="red" strokeDasharray="5 5" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано аналитика"
                        data= {
                            this.props.data.changeRequestById.analysisTimeSheetsByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentCumsum: item.timeSpentCumsum }
                            })
                        }
                        line fill="red"
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
                    <YAxis type="number" dataKey="timeSpentCumsum" />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>
                    {
                        (this.props.data.changeRequestById.plannedInstallDate) ?
                            <ReferenceLine x={ new Date(this.props.data.changeRequestById.plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.changeRequestById.developmentEstimate} stroke="green" strokeDasharray="5 5" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано разработка"
                        data= {
                            this.props.data.changeRequestById.developmentTimeSheetsByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentCumsum: item.timeSpentCumsum }
                            })
                        }
                        line fill="green"
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
                    <YAxis type="number" dataKey="timeSpentCumsum" />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>
                    {
                        (this.props.data.changeRequestById.plannedInstallDate) ?
                            <ReferenceLine x={ new Date(this.props.data.changeRequestById.plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.changeRequestById.testingEstimate} stroke="blue" strokeDasharray="5 5" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано тестирование"
                        data= {
                            this.props.data.changeRequestById.testingTimeSheetsByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentCumsum: item.timeSpentCumsum }
                            })
                        }
                        line fill="blue"
                    />
                </ScatterChart>

                <ul>
                    { this.props.data.changeRequestById.systemChangeRequests
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
                                { systemChangeRequest.stateCategory.id !== 3 ? `Осталось ${systemChangeRequest.timeLeft} ч ` : '' }
                                { systemChangeRequest.estimate === 0 && systemChangeRequest.stateCategory.id !== 3 ? `Оценка ${systemChangeRequest.estimate} ч ` : '' }

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