import React, {Component} from "react";
import { Legend, Tooltip, ReferenceLine, LineChart, Line, XAxis, YAxis } from "recharts";
import moment from 'moment';
import { getEveryMonthTicksBetweenTwoDates } from '../utils'

class ReengineeringByDatePeriodChart extends Component {
    render() {
        const planningPeriodEnd = this.props.planningPeriodEnd
        const today = (new Date()).getTime()
        const title = this.props.title
        const xAxisStart = this.props.xAxisStart
        const xAxisEnd = this.props.xAxisEnd
        const color = this.props.color
        const timeSpentPercentForReengineeringAndNotForReengineeringByDate = this.props.timeSpentPercentForReengineeringAndNotForReengineeringByDate

        return (
                <LineChart
                    width={ 1440 }
                    height={ 300 }
                    data={ timeSpentPercentForReengineeringAndNotForReengineeringByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentForReengineeringPercentCumsum: item.timeSpentForReengineeringPercentCumsum }
                        }).filter(item => {
                            return item.date >= xAxisStart
                        })
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
                            return Math.round(tick * 100) + " %";
                        }}
                    />
                    <Tooltip
                        labelFormatter={ (date) => moment(date).format('YYYY-MM-DD') }
                    />
                    <Legend />

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label={{ position: "left", value: "Сегодня" }} ifOverflow="extendDomain"/>

                    <ReferenceLine y={ 1 } stroke={ color } strokeDasharray="5 5" ifOverflow="extendDomain" label={{ position: 'top',  value: "100%" }} />

                    <Line
                        name={ title }
                        dataKey="timeSpentForReengineeringPercentCumsum"
                        stroke={ color }
                        dot={ false }
                    />
                </LineChart>
        );
    }
}

export default ReengineeringByDatePeriodChart;