import Header from './Header'
import styled from 'styled-components'

const SavedSchedulesPageHeader = styled.div`
    font-size: 50px;
    margin-top: 50px;
    margin-bottom: 50px;
    text-align: center;
`

const SavedSchedulesPage = (props) => {
    return (
        <>
            <Header login={props.login} user={props.user}/>
            <>
                <SavedSchedulesPageHeader>
                    To be implemented
                </SavedSchedulesPageHeader>
            </>
        </>
    )
}

export default SavedSchedulesPage
