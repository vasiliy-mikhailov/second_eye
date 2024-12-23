import React, {Component} from "react";
import { Legend, Tooltip, ReferenceLine, LineChart, Line, XAxis, YAxis } from "recharts";
import moment from 'moment';
import { getEveryMonthTicksBetweenTwoDates } from '../utils'

class TimeSheetsByDatePeriodChart extends Component {
    render() {
        const planningPeriodEnd = this.props.planningPeriodEnd
        const today = (new Date()).getTime()
        const title = this.props.title
        const xAxisStart = this.props.xAxisStart
        const xAxisEnd = this.props.xAxisEnd
        const color = this.props.color
        const timeSheetsByDate = this.props.timeSheetsByDate
        const estimate = this.props.estimate
        const calculatedFinishDate = new Date(this.props.calculatedFinishDate).getTime()

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
                                date: calculatedFinishDate,
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
                        domain={ [dataMin => xAxisStart, dataMax => xAxisEnd] }
                        tickFormatter={ (date) => moment(date).format('YYYY-MM-DD') }
                        ticks={ getEveryMonthTicksBetweenTwoDates(xAxisStart, xAxisEnd) }
                    />
                    <YAxis
                        type="number"
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <Tooltip
                        labelFormatter={ (date) => moment(date).format('YYYY-MM-DD') }
                    />
                    <Legend />

                    <ReferenceLine x={ new Date(planningPeriodEnd).getTime() } stroke="red" strokeDasharray="5 5" label={{ position: "left" }} ifOverflow="extendDomain"/>

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

export default TimeSheetsByDatePeriodChart;