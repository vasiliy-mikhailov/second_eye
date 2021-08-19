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
import {Box, Link} from "@material-ui/core";

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

        const plannedInstallDate = this.props.data.systemChangeRequestById.changeRequest.plannedInstallDate ? new Date(this.props.data.systemChangeRequestById.changeRequest.plannedInstallDate).getTime() : null
        const timeSheetsByDate = this.props.data.systemChangeRequestById.timeSheetsByDate

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
                    <Link href={ this.props.location.pathname }>
                        { this.props.data.systemChangeRequestById.id }
                    </Link> &nbsp;
                    { this.props.data.systemChangeRequestById.name } &nbsp;
                    { this.props.data.systemChangeRequestById.state.name } &nbsp;
                    <Link href={ this.props.data.systemChangeRequestById.url }>
                        [ источник ]
                    </Link>
                    <br />
                    Осталось { this.props.data.systemChangeRequestById.timeLeft } ч ( { (this.props.data.systemChangeRequestById.timeLeft / this.props.data.systemChangeRequestById.estimate * 100).toFixed(2) }% ) <br />
                    Сделано { this.props.data.systemChangeRequestById.timeSpent } ч <br />
                    Оценка { this.props.data.systemChangeRequestById.estimate } ч <br />
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
                    <YAxis
                        type="number"
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>

                    {
                        (plannedInstallDate) ?
                            <ReferenceLine x={ new Date(plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.systemChangeRequestById.estimate} stroke="black" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано всего"
                        data= {
                            this.props.data.systemChangeRequestById.timeSheetsByDate.map(item => {
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
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>

                    {
                        (plannedInstallDate) ?
                            <ReferenceLine x={ new Date(plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.systemChangeRequestById.analysisEstimate} stroke="red" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано аналитика"
                        data= {
                            this.props.data.systemChangeRequestById.analysisTimeSheetsByDate.map(item => {
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
                    <YAxis
                        type="number"
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>

                    {
                        (plannedInstallDate) ?
                            <ReferenceLine x={ new Date(plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.systemChangeRequestById.developmentEstimate} stroke="green" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано разработка"
                        data= {
                            this.props.data.systemChangeRequestById.developmentTimeSheetsByDate.map(item => {
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
                    <YAxis
                        type="number"
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={[1]} />
                    <Legend/>

                    {
                        (plannedInstallDate) ?
                            <ReferenceLine x={ new Date(plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

                    <ReferenceLine y={this.props.data.systemChangeRequestById.testingEstimate} stroke="blue" ifOverflow="extendDomain" />
                    <Scatter
                        name="Списано тестирование"
                        data= {
                            this.props.data.systemChangeRequestById.testingTimeSheetsByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentCumsum: item.timeSpentCumsum }
                            })
                        }
                        line fill="blue"
                    />
                </ScatterChart>
            </Box>
        );
    }
}

export default graphql(fetchSystemChangeRequest, {
    options: (props) => { return { variables: { id: props.match.params.id }}}
})(SystemChangeRequestDetail);