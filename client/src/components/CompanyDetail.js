import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";
import ReengineeringByDatePeriodChart from "./ReengineeringByDatePeriodChart";
import TimeSheetsByDateIssueChart from "./TimeSheetsByDateIssueChart";
import ValueByDatePeriodChart from "./ValueByDatePeriodChart";

const fetchCompanyWithIdOne = gql`
    query Company {
        planningPeriods {
            id 
            name
            start
            end
            calculatedFinishDate
            estimate
            timeLeft
            timeSpentChrononFte
            effortPerFunctionPoint
        }
        
        dedicatedTeams {
            id
            name
            timeLeft
            timeSpentChrononFte
            calculatedFinishDate
            queueLength
            timeSpentForReengineeringPercent
            effortPerFunctionPoint
        }
        
        companyById(id: 1) {
            id
            name
            estimate

            analysisTimeSpentChrononFte
            developmentTimeSpentChrononFte
            testingTimeSpentChrononFte
            managementTimeSpentChrononFte
            incidentFixingTimeSpentChrononFte
            nonProjectActivityTimeSpentChrononFte
            timeSpentChrononFte

            timeSpentForReengineeringPercent
            calculatedFinishDate
            
            timeSheetsByDate {
                date
                timeSpentCumsum
                timeSpentCumsumPrediction
                timeSpentWithoutValuePercentCumsum
                timeSpentWithValuePercentCumsum
                timeSpentForReengineeringPercentCumsum
                timeSpentNotForReengineeringPercentCumsum
            }
        }
        
        quarters {
            id
            key
            name
            timeSpentChrononFte
            effortPerFunctionPoint
        }
    }
`;

function CompanyDetail() {
    const {loading, error, data} = useQuery(fetchCompanyWithIdOne);

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const planningPeriods = data.planningPeriods
    const dedicatedTeams = data.dedicatedTeams
    const quarters = data.quarters

    const company = data.companyById
    const companyName = company.name
    const calculatedFinishDate = company.calculatedFinishDate
    const estimate = company.estimate

    const analysisTimeSpentChrononFte = company.analysisTimeSpentChrononFte
    const developmentTimeSpentChrononFte = company.developmentTimeSpentChrononFte
    const testingTimeSpentChrononFte = company.testingTimeSpentChrononFte
    const managementTimeSpentChrononFte = company.managementTimeSpentChrononFte
    const incidentFixingTimeSpentChrononFte = company.incidentFixingTimeSpentChrononFte
    const nonProjectActivityTimeSpentChrononFte = company.nonProjectActivityTimeSpentChrononFte
    const timeSpentChrononFte = company.timeSpentChrononFte

    const timeSheetsByDate = company.timeSheetsByDate
    const today = (new Date()).getTime()
    const firstTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[0].date).getTime() : null
    const lastTimeSheetDate = timeSheetsByDate.length > 0 ? new Date(timeSheetsByDate[timeSheetsByDate.length - 1].date).getTime() : null

    const allEdgeDates = [today]

    if (firstTimeSheetDate) {
        allEdgeDates.push(firstTimeSheetDate)
    }

    if (lastTimeSheetDate) {
        allEdgeDates.push(lastTimeSheetDate)
    }

    if (calculatedFinishDate) {
        allEdgeDates.push(new Date(calculatedFinishDate).getTime())
    }

    const xAxisStart = Math.min(...allEdgeDates) - 1000 * 60 * 60 * 24 * 28
    const xAxisEnd = Math.max(...allEdgeDates) + 1000 * 60 * 60 * 24 * 28

    const planningPeriodsTableContents = planningPeriods.slice()
        .sort((a, b) => ((a.start < b.start) ? 1 : ((a.start > b.start) ? -1 : 0)))
        .filter(a => a.estimate > 0)
        .map(planningPeriod => (
            {
                id: planningPeriod.id,
                estimate: planningPeriod.estimate,
                timeLeft: planningPeriod.timeLeft,
                name: planningPeriod.name,
                effortPerFunctionPoint: planningPeriod.effortPerFunctionPoint,
                calculatedFinishDate: planningPeriod.calculatedFinishDate,
                timeSpentChrononFte: planningPeriod.timeSpentChrononFte,
            }
        ))

    const planningPeriodsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/planningPeriods/${params.getValue(params.id, 'id')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'calculatedFinishDate',
            headerName: 'Расчетная дата завершения',
            width: 200,
            align: 'center',
        },
        {
            field: 'estimate',
            headerName: 'Оценка (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeLeft',
            headerName: 'Осталось (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'effortPerFunctionPoint',
            headerName: 'Затраты на ф.т.',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    const dedicatedTeamsTableContents = dedicatedTeams.slice()
        .sort((a, b) => ((a.name > b.name) ? 1 : ((a.name < b.name) ? -1 : 0)))
        .filter(dedicatedTeam => dedicatedTeam.timeLeft > 0)
        .map(dedicatedTeam => (
            {
                id: dedicatedTeam.id,
                name: dedicatedTeam.name,
                timeLeft: dedicatedTeam.timeLeft,
                timeSpentChrononFte: dedicatedTeam.timeSpentChrononFte,
                calculatedFinishDate: dedicatedTeam.calculatedFinishDate,
                queueLength: dedicatedTeam.queueLength,
                timeSpentForReengineeringPercent: dedicatedTeam.timeSpentForReengineeringPercent,
                effortPerFunctionPoint: dedicatedTeam.effortPerFunctionPoint,
            }
        ))

    const dedicatedTeamsTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/dedicatedTeams/${params.getValue(params.id, 'id')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'calculatedFinishDate',
            headerName: 'Расчетная дата завершения',
            width: 200,
            align: 'center',
        },
        {
            field: 'queueLength',
            headerName: 'Длина очереди (мес)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeLeft',
            headerName: 'Осталось (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentForReengineeringPercent',
            headerName: 'Затраты на технологическое перевооружение и исправление проблем (%)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value * 100).toLocaleString(undefined, {
                minimumFractionDigits: 1,
                maximumFractionDigits: 1
            }),
        },
        {
            field: 'effortPerFunctionPoint',
            headerName: 'Затраты на ф.т.',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    const quartersTableContents = quarters.slice()
        .sort((a, b) => ((a.start < b.start) ? 1 : ((a.start > b.start) ? -1 : 0)))
        .map(quarter => (
            {
                id: quarter.id,
                key: quarter.key,
                name: quarter.name,
                timeSpentChrononFte: quarter.timeSpentChrononFte,
                effortPerFunctionPoint: quarter.effortPerFunctionPoint,
            }
        ))

    const quartersTableColumns = [
        {
            field: 'name',
            headerName: 'Название',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/quarters/${params.getValue(params.id, 'key')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность FTE',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'effortPerFunctionPoint',
            headerName: 'Затраты на ф.т.',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    return (
        <Box>
            <Typography variant="body" noWrap>
                Компания {companyName}
                <br/>
                Расчетная дата завершения {calculatedFinishDate}
                <br/>
                FTE (аналитика, разработка, тестирование, управление, инциденты, непроектная
                деятельность): {timeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})} <br/>
                - аналитика {analysisTimeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})} <br/>
                - разработка {developmentTimeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})}
                <br/>
                - тестирование {testingTimeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})} <br/>
                - управление {managementTimeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})} <br/>
                - инциденты {incidentFixingTimeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})}
                <br/>
                - непроизводственная (текущая)
                деятельность {nonProjectActivityTimeSpentChrononFte.toLocaleString(undefined, {maximumFractionDigits: 0})}
                <br/>
                <br/>
            </Typography>

            <TimeSheetsByDateIssueChart
                title="Фактический объем работ: Аналитика + Разработка + Тестирование + Управление + Инциденты + Текущая деятельность"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSheetsByDate={timeSheetsByDate}
                estimate={estimate}
                calculatedFinishDate={calculatedFinishDate}
            />

            <Typography variant="body1">
                <RouterLink to={`/capacityAndQueue`}>
                    Очереди по командам
                </RouterLink>
            </Typography>
            <br/>


            <ValueByDatePeriodChart
                title="Доля списаний на задачи без бизнес-ценности"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSpentPercentWithValueAndWithoutValueByDate={timeSheetsByDate}
            />

            <ReengineeringByDatePeriodChart
                planningPeriodEnd={xAxisEnd}
                title="Доля списаний на задачи технологического перевооружения и исправления проблем"
                xAxisStart={xAxisStart}
                xAxisEnd={xAxisEnd}
                color="black"
                timeSpentPercentForReengineeringAndNotForReengineeringByDate={timeSheetsByDate}
            />

            <Typography variant="h6" noWrap>
                Выделенные команды
            </Typography>

            <div>
                <DataGridPro
                    rows={dedicatedTeamsTableContents}
                    columns={dedicatedTeamsTableColumns}
                    autoHeight
                />
            </div>

            <br/>

            <Typography variant="body1">
                <RouterLink to={`/projectTeams`}>
                    Проектные команды одним списком
                </RouterLink>
            </Typography>
            <br/>
            <Typography variant="body1">
                <RouterLink to={`/projectManagers`}>
                    Менеджеры проектов одним списком
                </RouterLink>
            </Typography>
            <br/>

            <Typography variant="body1">
                <RouterLink to={`/systems`}>
                    Системы одним списком
                </RouterLink>
            </Typography>
            <br/>

            <Typography variant="h6" noWrap>
                Кварталы
            </Typography>

            <div>
                <DataGridPro
                    rows={quartersTableContents}
                    columns={quartersTableColumns}
                    autoHeight
                />
            </div>

            <Typography variant="h6" noWrap>
                Периоды
            </Typography>

            <div>
                <DataGridPro
                    rows={ planningPeriodsTableContents }
                    columns={ planningPeriodsTableColumns }
                    autoHeight
                />
            </div>
            <br/>
        </Box>
    );
}

export default CompanyDetail;