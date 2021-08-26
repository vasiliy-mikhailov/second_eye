import React, {Component} from "react";
import { Legend, ReferenceLine, Scatter, ScatterChart, XAxis, YAxis, ZAxis } from "recharts";
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

        return (
                <ScatterChart
                    width={ 1440 }
                    height={ 200 }
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
                        dataKey="timeSpentCumsum"
                        tickFormatter={ tick => {
                            return tick.toLocaleString();
                        }}
                    />
                    <ZAxis type="number" range={ [1] } />
                    <Legend/>

                    {
                        (plannedInstallDate) ?
                            <ReferenceLine x={ new Date(plannedInstallDate).getTime() } stroke="red" strokeDasharray="5 5" label="Плановая дата установки" ifOverflow="extendDomain"/> :
                            ""
                    }

                    <ReferenceLine x={ today } stroke="blue" strokeDasharray="5 5" label="Сегодня" ifOverflow="extendDomain"/>

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

export default TimeSheetsByDateIssueChart;