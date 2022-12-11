import { useEffect, useState } from 'react'
import Header from './Header'
import instance from '../../src/Client'
import styled from 'styled-components'
 import {
    Button
} from '@mui/material'


const GenerateSchedulePageHeader = styled.div`
    font-size: 50px;
    margin-top: 50px;
    margin-bottom: 50px;
    text-align: center;
`

const GenerateSchedulePageBody = styled.div`
    width: 320px;
    margin: 0 auto;
    color: #2c3e50;
    font-size: 20px;
    text-align: center;
`

const GenerateSchedulePageLine = styled.div`
    margin-bottom: 10px;
    background-color: #ecf0f1;
`



const GenerateSchedulePage = (props) => {
    const [data, setData] = useState(null)

    const handleClick = () => {
        console.log("Button clicked")
    }

    useEffect(() => {
        instance.get("http://localhost:8001/api/v1/schedule/generate")
        .then((res) => {
            console.log(res.data)
            if (res.data['status'] === 200){
                setData(res.data['greedy_schedule'])
            } else {

            }
        })
        .catch((error) => {
            console.log(error)
        })
    }, [])
    if (data === null) return <></>
    return (
        <>
            <Header login={props.login} user={props.user}/>
            {/* <>
                GenerateSchedulePage
            </> */}
            <GenerateSchedulePageHeader>
                Greedy Schedule
            </GenerateSchedulePageHeader>

            <GenerateSchedulePageBody>
                {
                    data.map((e) => 
                        <GenerateSchedulePageLine>
                            {e['old_code']}: {e['title_en']}
                        </GenerateSchedulePageLine>
                    )
                }
            <Button
                variant='contained'
                style={{
                    "height": "100px",
                    "width": "200px",
                    "marginTop": "20px",
                    "fontSize": "30px"
                }}
                onClick={handleClick}
            >
                Save Schedule
            </Button>
            </GenerateSchedulePageBody>
            
        </>
    )
}

export default GenerateSchedulePage
