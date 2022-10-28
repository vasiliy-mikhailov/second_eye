import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box} from "@material-ui/core";
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DataGridPro, GridToolbarContainer, GridToolbarExport, } from '@mui/x-data-grid-pro';
import {Link as RouterLink} from "react-router-dom";

const fetchCapacityAndQueue = gql`
    query capacityAndQueue {
        companies {
            id
            name         
            queueLength
        }
        
        dedicatedTeams {
            id
            name
            queueLength
        }
        
        projectTeams {
            id
            name
            queueLength
            
            dedicatedTeam {
                name
            }
        }
    }
`;

function ToolBarWithExport() {
  return (
    <GridToolbarContainer>
        <GridToolbarExport
          csvOptions={{
              delimiter: ";",
              utf8WithBom: true,
          }}
        />


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
                    queueLength: Math.round(company.queueLength),
                }
            }
        )

        const dedicatedTeamsQueue = dedicatedTeams.slice().map(
            dedicatedTeam => {
                return {
                    id: dedicatedTeam.id,
                    name: dedicatedTeam.name,
                    queueLength: Math.round(dedicatedTeam.queueLength),
                }
            }
        )

        const projectTeamsQueue = projectTeams.slice().map(
            projectTeam => {
                return {
                    id: projectTeam.id,
                    name: projectTeam.name + " : " + projectTeam.dedicatedTeam.name,
                    queueLength: Math.round(projectTeam.queueLength),
                }
            }
        )

        const top10ProjectTeams = projectTeamsQueue.sort(
            function(a, b) {
                return b.queueLength - a.queueLength
            }
        ).slice(0, 9)

        const top20To50ProjectTeams = projectTeamsQueue.sort(
            function(a, b) {
                return b.queueLength - a.queueLength
            }
        ).slice(10)

        const topDedicatedTeams = dedicatedTeamsQueue.sort(
                        function(a, b) {
                return b.queueLength - a.queueLength
            }
        )

        const topDedicatedTeamsColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/dedicatedTeams/${ params.getValue(params.id, 'id') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'queueLength',
                headerName: 'Очередь (мес)',
                flex: 1,
            },
        ];

        const topProjectTeams = projectTeamsQueue.sort(
                        function(a, b) {
                return b.queueLength - a.queueLength
            }
        )

        const topProjectTeamsColumns = [
            {
                field: 'name',
                headerName: 'Название',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/projectTeams/${ params.getValue(params.id, 'id') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'queueLength',
                headerName: 'Очередь (мес)',
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
                    data={topDedicatedTeams}
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
                    <Bar dataKey="queueLength" name={"Очередь (мес)"} />
                </BarChart>

                <div>
                    <DataGridPro
                        rows={topDedicatedTeams}
                        columns={topDedicatedTeamsColumns}
                        components={{
                            Toolbar: ToolBarWithExport,
                        }}
                        autoHeight
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
                    <Bar dataKey="queueLength" name={"Очередь (мес)"} />
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
                    <Bar dataKey="queueLength" name={"Очередь (мес)"} />
                </BarChart>

                <div>
                    <DataGridPro
                        rows={topProjectTeams}
                        columns={topProjectTeamsColumns}
                        components={{
                            Toolbar: ToolBarWithExport,
                        }}
                        autoHeight
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchCapacityAndQueue)(CapacityAndQueue);