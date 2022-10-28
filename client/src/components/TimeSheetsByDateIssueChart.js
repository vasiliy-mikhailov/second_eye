import React, {Component} from "react";
import { Legend, Tooltip, ReferenceLine, LineChart, Line, XAxis, YAxis } from "recharts";
import moment from 'moment';
import { getEveryMonthTicksBetweenTwoDates } from '../utils'

class TimeSheetsByDateIssueChart extends Component {
    render() {
        const plannedInstallDate = this.props.plannedInstallDate
        const today = (new Date()).getTime()
        const title = this.props.title
        const xAxisStart = this.props.xAxisStart
        const xAxisEnd = this.props.xAxisEnd
        const color = this.props.color
        const timeSheetsByDate = this.props.timeSheetsByDate
        const estimate = this.props.estimate
        const calculatedFinishDate = this.props.calculatedFinishDate

        return (
                <LineChart
                    width={ 1440 }
                    height={ 300 }
                    data={ timeSheetsByDate.map(item => {
                            return {
                                date: new Date(item.date).getTime(),
                                timeSpentCumsum: Math.round(item.timeSpentCumsum),
                                timeSpentCumsumPrediction: Math.round(item.timeSpentCumsumPrediction)
                            }
                        }).filter(item => {
                            return item.date >= xAxisStart
                        }).concat([{
                                date: new Date(calculatedFinishDate).getTime(),
                                timeSpentCumsum: null,
                                timeSpentCumsumPrediction: Math.round(estimate)
                            }]
                        )
                    }
                    margin={{
                        left: 20,
                        top: 50
                    }}
                >
                    <XAxis
                        dataKey="date"
                        type="number"
                        domain={ [xAxisStart, xAxisEnd] }
                        allowDataOverflow={ true }
                        tickFormatter={ (date) => moment(date).format('YYYY-MM-DD') }
                        ticks={ getEveryMonthTicksBetweenTwoDates(xAxisStart, xAxisEnd) }
                    />
                    <YAxis
                        type="number"
                        domain={ [dataMin => 0, dataMax => estimate] }
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <Tooltip
                        labelFormatter={ (date) => moment(date).format('YYYY-MM-DD') }
                    />
                    <Legend />

                    {
                        (plannedInstallDate) ?
                            <ReferenceLine x={ new Date(plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label={{ position: "right", value: "Плановая дата установки" }} ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label={{ position: "left", value: "Сегодня" }} ifOverflow="extendDomain"/>

                    <ReferenceLine y={ estimate } stroke={ color } strokeDasharray="5 5" ifOverflow="extendDomain" label={{ position: 'top',  value: "Плановый объем работ " + Math.round(estimate).toLocaleString() + " ч" }} />

                    <Line
                        name={ title }
                        dataKey="timeSpentCumsum"
                        stroke={ color }
                        dot={false}
                    />

                    <Line
                        name={ "Тренд" }
                        dataKey="timeSpentCumsumPrediction"
                        stroke={ color }
                        dot={false}
                        strokeDasharray="1 5"
                    />
                </LineChart>
        );
    }
}

export default TimeSheetsByDateIssueChart;