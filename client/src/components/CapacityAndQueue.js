import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DataGrid, GridToolbarContainer, GridToolbarExport, } from '@material-ui/data-grid';

const fetchCapacityAndQueue = gql`
    query capacityAndQueue {
        companies {
            id
            name
            actualChangeRequestCapacity
            actualAnalysisCapacity
            actualDevelopmentCapacity
            actualTestingCapacity
            
            timeLeft
            analysisTimeLeft
            developmentTimeLeft
            testingTimeLeft
            
            queueLength
            analysisQueueLength
            developmentQueueLength
            testingQueueLength
        }
        
        dedicatedTeams {
            id
            name
            actualChangeRequestCapacity
            actualAnalysisCapacity
            actualDevelopmentCapacity
            actualTestingCapacity
            
            timeLeft
            analysisTimeLeft
            developmentTimeLeft
            testingTimeLeft
            
            queueLength
            analysisQueueLength
            developmentQueueLength
            testingQueueLength
        }
        
        projectTeams {
            id
            name
            actualChangeRequestCapacity
            actualAnalysisCapacity
            actualDevelopmentCapacity
            actualTestingCapacity
            
            timeLeft
            analysisTimeLeft
            developmentTimeLeft
            testingTimeLeft
            
            queueLength
            analysisQueueLength
            developmentQueueLength
            testingQueueLength
            
            dedicatedTeam {
                name
            }
        }
    }
`;

function ToolBarWithExport() {
  return (
    <GridToolbarContainer>
      <GridToolbarExport />
    </GridToolbarContainer>
  );
}

class CapacityAndQueue extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const companies = this.props.data.companies
        const dedicatedTeams = this.props.data.dedicatedTeams
        const projectTeams = this.props.data.projectTeams

        const companiesQueue = companies.slice().map(
            company => {
                return {
                    id: company.id,
                    name: company.name,
                    queueLength: Math.round(company.queueLength / 22),
                    analysisQueueLength: Math.round(company.analysisQueueLength / 22),
                    developmentQueueLength: Math.round(company.developmentQueueLength / 22),
                    testingQueueLength: Math.round(company.testingQueueLength / 22)
                }
            }
        )

        const dedicatedTeamsQueue = dedicatedTeams.slice().map(
            dedicatedTeam => {
                return {
                    id: dedicatedTeam.id,
                    name: dedicatedTeam.name,
                    queueLength: Math.round(dedicatedTeam.queueLength / 22),
                    analysisQueueLength: Math.round(dedicatedTeam.analysisQueueLength / 22),
                    developmentQueueLength: Math.round(dedicatedTeam.developmentQueueLength / 22),
                    testingQueueLength: Math.round(dedicatedTeam.testingQueueLength / 22)
                }
            }
        )

        const projectTeamsQueue = projectTeams.slice().map(
            projectTeam => {
                return {
                    id: projectTeam.id,
                    name: projectTeam.name + " : " + projectTeam.dedicatedTeam.name,
                    queueLength: Math.round(projectTeam.queueLength / 22),
                    analysisQueueLength: Math.round(projectTeam.analysisQueueLength / 22),
                    developmentQueueLength: Math.round(projectTeam.developmentQueueLength / 22),
                    testingQueueLength: Math.round(projectTeam.testingQueueLength / 22)
                }
            }
        )

        const top10ProjectTeams = projectTeamsQueue.sort(
            function(a, b) {
                return Math.max(
                    b.queueLength,
                    b.analysisQueueLength,
                    b.developmentQueueLength,
                    b.testingQueueLength
                ) - Math.max(
                    a.queueLength,
                    a.analysisQueueLength,
                    a.developmentQueueLength,
                    a.testingQueueLength
                )
            }
        ).slice(0, 9)

        const top20To50ProjectTeams = projectTeamsQueue.sort(
            function(a, b) {
                return Math.max(
                    b.queueLength,
                    b.analysisQueueLength,
                    b.developmentQueueLength,
                    b.testingQueueLength
                ) - Math.max(
                    a.queueLength,
                    a.analysisQueueLength,
                    a.developmentQueueLength,
                    a.testingQueueLength
                )
            }
        ).slice(10)

        const topDedicatedTeamsWithCompanies = companiesQueue.concat(dedicatedTeamsQueue).sort(
                        function(a, b) {
                return Math.max(
                    b.queueLength,
                    b.analysisQueueLength,
                    b.developmentQueueLength,
                    b.testingQueueLength
                ) - Math.max(
                    a.queueLength,
                    a.analysisQueueLength,
                    a.developmentQueueLength,
                    a.testingQueueLength
                )
            }
        )

        const topDedicatedTeamsWithCompaniesColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
            },
            {
                field: 'queueLength',
                headerName: 'Очередь (мес)',
                flex: 1,
            },
            {
                field: 'analysisQueueLength',
                headerName: 'Очередь аналитики (мес)',
                flex: 1,
            },
            {
                field: 'developmentQueueLength',
                headerName: 'Очередь разработки (мес)',
                flex: 1,
            },
            {
                field: 'testingQueueLength',
                headerName: 'Очередь тестирования (мес)',
                flex: 1,
            },
        ];

        const topProjectTeams = projectTeamsQueue.sort(
                        function(a, b) {
                return Math.max(
                    b.queueLength,
                    b.analysisQueueLength,
                    b.developmentQueueLength,
                    b.testingQueueLength
                ) - Math.max(
                    a.queueLength,
                    a.analysisQueueLength,
                    a.developmentQueueLength,
                    a.testingQueueLength
                )
            }
        )

        const topProjectTeamsColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
            },
            {
                field: 'queueLength',
                headerName: 'Очередь (мес)',
                flex: 1,
            },
            {
                field: 'analysisQueueLength',
                headerName: 'Очередь аналитики (мес)',
                flex: 1,
            },
            {
                field: 'developmentQueueLength',
                headerName: 'Очередь разработки (мес)',
                flex: 1,
            },
            {
                field: 'testingQueueLength',
                headerName: 'Очередь тестирования (мес)',
                flex: 1,
            },
        ];

        return (
            <Box>
                <Typography variant="body1">
                    Выделенные команды (месяцы)
                </Typography>
                <BarChart
                    width={1600}
                    height={800}
                    data={topDedicatedTeamsWithCompanies}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 30,
                        bottom: 400,
                    }}
                    barCategoryGap="10%"
                    barGap="0%"
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" interval={0} angle={-90} textAnchor="end" fontSize={10} fontFamily={"Helvetica"} />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip />
                    <Legend layout="horizontal" verticalAlign="top" align="center" />
                    <Bar dataKey="analysisQueueLength" fill="red" name={"Аналитика"} />
                    <Bar dataKey="developmentQueueLength" fill="green" name={"Разработка"} />
                    <Bar dataKey="testingQueueLength" fill="blue" name={"Тестирование"} />
                </BarChart>

                <div style={{ height: 400, width: '100%' }}>
                    <DataGrid
                        rows={topDedicatedTeamsWithCompanies}
                        columns={topDedicatedTeamsWithCompaniesColumns}
                        components={{
                            Toolbar: ToolBarWithExport,
                        }}
                    />
                </div>

                <Typography variant="body1">
                    Top-10 проектных команд (месяцы)
                </Typography>
                <BarChart
                    width={1600}
                    height={800}
                    data={top10ProjectTeams}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 30,
                        bottom: 400,
                    }}
                    barCategoryGap="10%"
                    barGap="0%"
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" interval={0} angle={-90} textAnchor="end" fontSize={10} fontFamily={"Helvetica"} />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip />
                    <Legend layout="horizontal" verticalAlign="top" align="center" />
                    <Bar dataKey="analysisQueueLength" fill="red" name={"Аналитика"} />
                    <Bar dataKey="developmentQueueLength" fill="green" name={"Разработка"} />
                    <Bar dataKey="testingQueueLength" fill="blue" name={"Тестирование"} />
                </BarChart>

                <Typography variant="body1">
                    Остальные проектные команды (месяцы)
                </Typography>
                <BarChart
                    width={1600}
                    height={800}
                    data={top20To50ProjectTeams}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 30,
                        bottom: 400,
                    }}
                    barCategoryGap="10%"
                    barGap="0%"
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" interval={0} angle={-90} textAnchor="end" fontSize={10} fontFamily={"Helvetica"} />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip />
                    <Legend layout="horizontal" verticalAlign="top" align="center" />
                    <Bar dataKey="analysisQueueLength" fill="red" name={"Аналитика"} />
                    <Bar dataKey="developmentQueueLength" fill="green" name={"Разработка"} />
                    <Bar dataKey="testingQueueLength" fill="blue" name={"Тестирование"} />
                </BarChart>

                <div style={{ height: 400, width: '100%' }}>
                    <DataGrid
                        rows={topProjectTeams}
                        columns={topProjectTeamsColumns}
                        components={{
                            Toolbar: ToolBarWithExport,
                        }}
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchCapacityAndQueue)(CapacityAndQueue);