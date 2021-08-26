import React, {Component} from "react";
import { Legend, ReferenceLine, Scatter, ScatterChart, XAxis, YAxis, ZAxis } from "recharts";
import moment from 'moment';
import { getEveryMonthTicksBetweenTwoDates } from '../utils'

class TimeSheetsByDatePeriodChart extends Component {
    render() {
        const planningPeriodStart = this.props.planningPeriodStart
        const planningPeriodEnd = this.props.planningPeriodEnd
        const today = (new Date()).getTime()
        const title = this.props.title
        const xAxisStart = this.props.xAxisStart
        const xAxisEnd = this.props.xAxisEnd
        const color = this.props.color
        const timeSheetsByDate = this.props.timeSheetsByDate
        const estimate = this.props.estimate

        return (
                <ScatterChart
                    width={ 1440 }
                    height={ 200 }
                >
                    <XAxis
                        dataKey="date"
                        type="number"
                        domain={ [dataMin => xAxisStart, dataMax => xAxisEnd] }
                        tickFormatter={ (date) => moment(date).format('MMM') }
                        ticks={ getEveryMonthTicksBetweenTwoDates(xAxisStart, xAxisEnd) }
                    />
                    <YAxis
                        type="number"
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={ [1] } />
                    <Legend/>

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" />

                    <ReferenceLine y={ estimate } stroke={ color } strokeDasharray="5 5" ifOverflow="extendDomain" label="Оценка" />

                    <Scatter
                        name={ title }
                        data={ timeSheetsByDate.map(item => {
                                return { date: new Date(item.date).getTime(), timeSpentCumsum: item.timeSpentCumsum }
                            })
                        }
                        line fill={ color }
                    />
                </ScatterChart>
        );
    }
}

export default TimeSheetsByDatePeriodChart;