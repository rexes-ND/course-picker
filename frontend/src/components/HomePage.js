import Header from './Header';
import styled from 'styled-components';
import {Link} from 'react-router-dom'
import {
    Button
} from '@mui/material'
const HomePageBody = styled.div`
    background-color: #ecf0f1;
    margin-top: 20px;
    width: 970px;
    margin-left: auto;
    margin-right: auto;
`

const HomePageHeader = styled.h1`
    color: #2c3e50;
    font-size: 68px;
    text-align: center;
    margin-top: 20px;
    padding-top: 20px;
    margin-bottom: 10px;
`

const HomePageText = styled.div`
    text-align: center;
    font-size: 23px;
    margin-bottom: 10px;
`

const ButtonContainer = styled.div`
    display: flex;
    margin-left: auto;
    margin-right: auto;
    width: 500px;
    justify-content: space-between;
    margin-top: 50px;
`


const HomePage = (props) => {
    return (
        <>
            <Header login={props.login} user={props.user}/>
            <HomePageBody>
                <HomePageHeader>
                    Automatic Course Picker
                </HomePageHeader>
                <HomePageText>
                    Welcome to Automatic Course Picker!
                </HomePageText>
                <HomePageText>
                    You can use following services using Automatic Course Picker
                </HomePageText>
                <ButtonContainer>
                    <Link to={(props.user["majorType"]==="" || props.user["major"]==="" || props.user["minor"]==="")?"/user":"/generate"} style={{ textDecoration: 'none' }}>
                        <Button
                            variant='contained'
                            style={{
                                "height": "100px",
                                "width": "200px",
                                "marginBottom": "20px",
                                "fontSize": "30px"
                            }}
                        >
                            Generate Schedule
                        </Button>
                    </Link>
                    <Link to={(props.user["majorType"]==="" || props.user["major"]==="" || props.user["minor"]==="")?"/user":"/saved"} style={{ textDecoration: 'none' }}>
                        <Button
                            variant='contained'
                            style={{
                                "height": "100px",
                                "width": "200px",
                                "marginBottom": "20px",
                                "fontSize": "30px"
                            }}
                        >
                            Saved Schedules
                        </Button>
                    </Link>
                </ButtonContainer>
            </HomePageBody>
           
        </>
    )
}

export default HomePage