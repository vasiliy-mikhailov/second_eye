import React from "react";
import {gql, useQuery} from '@apollo/client';
import Typography from '@material-ui/core/Typography';
import {Box, Link} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import {DataGridPro} from "@mui/x-data-grid-pro";

const fetchSystemById = gql`
    query SystemById($id: Int!) {
        systemById(id: $id) {
            id
            estimate
            timeLeft
            name
            timeSpentChrononFte
            timeSpentChronon
            
            persons {
                id
                
                person {
                    id
                    key
                    name
                    isActive
                    timeSpentChrononFte
                }
                
                timeSpent
                
                timeSpentChrononFte
            }
        }
    }
`;

function SystemDetail() {
    const {systemId} = useParams();
    const {loading, error, data} = useQuery(fetchSystemById, {
        variables: {systemId: systemId}
    });

    if (loading) return 'Loading ...'

    if (error) return `Error! ${error.message}`

    const system = data.systemById

    const systemName = system.name
    const estimate = system.estimate

    const persons = system.persons

    const personsTableContents = persons.slice()
        .sort((a, b) => (
            (a.timeSpentChrononFte > b.timeSpentChrononFte) ? -1 : (
                (a.timeSpentChrononFte == b.timeSpentChrononFte) ? 0 : 1
            )
        ))
        .map(person => (
            {
                id: person.id,
                personId: person.person.id,
                key: person.person.key,
                name: person.person.name,
                timeSpent: person.timeSpent,
                timeSpentChrononFteTotal: person.person.timeSpentChrononFte,
                timeSpentChrononFte: person.timeSpentChrononFte,
                isActive: person.person.isActive,
            }
        ))

    const personsTableColumns = [
        {
            field: 'name',
            headerName: 'ФИО',
            flex: 1,
            renderCell: (params) => (
                <RouterLink to={`/persons/${params.getValue(params.id, 'key')}`}>
                    {params.getValue(params.id, 'name')}
                </RouterLink>
            ),
        },
        {
            field: 'isActive',
            headerName: 'Активный',
            flex: 1,
            renderCell: (params) => (
                params.getValue(params.id, 'isActive') ? "Да" : "Нет"
            ),
        },
        {
            field: 'timeSpent',
            headerName: 'Трудозатраты (ч)',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => value.toLocaleString(undefined, {maximumFractionDigits: 0}),
        },
        {
            field: 'timeSpentChrononFte',
            headerName: 'Трудомощность на эту систему',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
        {
            field: 'timeSpentChrononFteTotal',
            headerName: 'Трудомощность на все системы',
            width: 200,
            align: 'right',
            valueFormatter: ({value}) => (value).toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }),
        },
    ];

    return (
        <Box>
            <Typography variant="body" noWrap>
                Система {systemName} &nbsp;
                <br/>
                <br/>
            </Typography>

            <Typography variant="h6" noWrap>
                Команда
            </Typography>
            <div>
                <DataGridPro
                    rows={personsTableContents}
                    columns={personsTableColumns}
                    autoHeight
                />
            </div>
        </Box>
    );
}

export default SystemDetail;