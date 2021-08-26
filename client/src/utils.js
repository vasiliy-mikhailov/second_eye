import moment from 'moment';

const getEveryMonthTicksBetweenTwoDates = (start, end) => {
    var startMoment = moment(start).startOf("month")
    var endMoment = moment(end).endOf("month")
    var result = [];

    var momentIndex = startMoment
    while (endMoment > momentIndex) {
        result.push(momentIndex.toDate());
        momentIndex.add(1, 'month');
    }

    return result
}

export { getEveryMonthTicksBetweenTwoDates }