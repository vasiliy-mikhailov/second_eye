import React from "react";
import {gql, useQuery} from '@apollo/client';
import {graphql} from '@apollo/client/react/hoc';
import Typography from '@material-ui/core/Typography';
import {Link as RouterLink, NavLink, useParams} from "react-router-dom"
import {Box} from "@material-ui/core";
import {DataGridPro, GridToolbarContainer, GridToolbarExport} from "@mui/x-data-grid-pro";

function ToolBarWithExport() {
    return (
        <GridToolbarContainer>
            <GridToolbarExport/>
        </GridToolbarContainer>
    );
}

const fetchPersonList = gql`
    query Persons {
        persons {
            id 
            name
            mainProjectTeam {
                id
                name
                dedicatedTeam {
                    id
                    name
                }
            }
        }
    }
`;

function PersonList() {
    const {loading, error, data} = useQuery(fetchPersonList);

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const persons = data.persons

    const personsTableContents = persons.slice()
        .filter((person) => (
            person.mainProjectTeam.id != -1
        ))
        .sort((a, b) => (
            (a.name > b.name) ? 1 : (
                (a.name == b.name) ? 0 : -1
            )
        ))
        .map(person => (
            {
                id: person.id,
                name: person.name,
                mainProjectTeamId: person.mainProjectTeam.id,
                mainProjectTeamName: person.mainProjectTeam.name,
                mainDedicatedTeamId: person.mainProjectTeam.dedicatedTeam.id,
                mainDedicatedTeamName: person.mainProjectTeam.dedicatedTeam.name,
            }
        ))

    const personsTableColumns = [
        {
            field: 'name',
            headerName: 'Имя',
            flex: 1,
        },
        {
            field: 'mainProjectTeamName',
            headerName: 'Основная проектная команда',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/projectTeams/${params.getValue(params.id, 'mainProjectTeamId')}`}>
                    {params.getValue(params.id, 'mainProjectTeamName')}
                </RouterLink>
            ),
        },
        {
            field: 'mainDedicatedTeamName',
            headerName: 'Основная выделенная команда',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/dedicatedTeams/${params.getValue(params.id, 'mainDedicatedTeamId')}`}>
                    {params.getValue(params.id, 'mainDedicatedTeamName')}
                </RouterLink>
            ),
        },
    ];

    return (
        <Box>
            <Typography variant="h6" noWrap>
                Команда
            </Typography>
            <div>
                <DataGridPro
                    rows={personsTableContents}
                    columns={personsTableColumns}
                    components={{
                        Toolbar: ToolBarWithExport,
                    }}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default graphql(fetchPersonList)(PersonList);