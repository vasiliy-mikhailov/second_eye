import React, {Component} from "react";
import {gql} from '@apollo/client';
import { graphql } from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {DataGridPro, GridToolbarContainer, GridToolbarExport,} from '@mui/x-data-grid-pro';

const fetchProjectManagers = gql`
    query ProjectManagers {
        projectManagers {
            id
            
            name
            
            isActive
            
            analysisTimeSpentChrononFte
            developmentTimeSpentChrononFte
            testingTimeSpentChrononFte
            managementTimeSpentChrononFte
            incidentFixingTimeSpentChrononFte
            nonProjectActivityTimeSpentChrononFte
            
            timeSpentChrononFte
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

class ProjectManagerList extends Component {
    render() {
        if (this.props.data.loading) { return <div>Loading ...</div> }

        const projectManagers = this.props.data.projectManagers

        const projectManagersTableContents = projectManagers.slice()
            .sort((a, b) => ((a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : ((a.timeSpentChrononFte < b.timeSpentChrononFte) ? 1 : 0)))
            .map(projectManager => (
                    {
                        id: projectManager.id,
                        name: projectManager.name,
                        isActive: projectManager.isActive,
                        timeSpentChrononFte: projectManager.timeSpentChrononFte,
                        analysisTimeSpentChrononFte: projectManager.analysisTimeSpentChrononFte,
                        developmentTimeSpentChrononFte: projectManager.developmentTimeSpentChrononFte,
                        testingTimeSpentChrononFte: projectManager.testingTimeSpentChrononFte,
                        managementTimeSpentChrononFte: projectManager.managementTimeSpentChrononFte,
                        incidentFixingTimeSpentChrononFte: projectManager.incidentFixingTimeSpentChrononFte,
                        nonProjectActivityTimeSpentChrononFte: projectManager.nonProjectActivityTimeSpentChrononFte,
                    }
            ))

        const projectManagersTableColumns = [
            {
                field: 'name',
                headerName: 'ФИО',
                flex: 1,
                renderCell: (params) => (
                    <RouterLink to={ `/projectManagers/${ params.getValue(params.id, 'id') }` }>
                        { params.getValue(params.id, 'name') }
                    </RouterLink>
                ),
            },
            {
                field: 'isActive',
                headerName: 'Работает',
                flex: 1,
            },
            {
                field: 'timeSpentChrononFte',
                headerName: 'FTE команд за последний период',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'analysisTimeSpentChrononFte',
                headerName: 'Аналитика, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'developmentTimeSpentChrononFte',
                headerName: 'Разработка, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'testingTimeSpentChrononFte',
                headerName: 'Тестирование, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'managementTimeSpentChrononFte',
                headerName: 'Управление, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'incidentFixingTimeSpentChrononFte',
                headerName: 'Устранение инцидентов, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
            {
                field: 'nonProjectActivityTimeSpentChrononFte',
                headerName: 'Непроизводственная (текущая) деятельность, FTE',
                width: 200,
                align: 'right',
                valueFormatter: ({ value }) => (value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2}),
            },
        ];

        return (
            <Box>
                <Typography variant="h6" noWrap>
                    Менеджеры проектов
                </Typography>

                <div>
                    <DataGridPro
                        rows={ projectManagersTableContents }
                        columns={ projectManagersTableColumns }
                        autoHeight
                        components={{
                            Toolbar: ToolBarWithExport,
                        }}
                    />
                </div>
            </Box>
        );
    }
}

export default graphql(fetchProjectManagers)(ProjectManagerList);