import Header from './Header';
import styled from 'styled-components';

const LoginButton = styled.button`
    height: 50px;
    width: 100%;
    cursor: pointer;
    font-size: 18px;
    color: white;
    background-color: rgb(1, 67, 143);
    border-color: rgb(1, 67, 143);
    border: 1px solid transparent;
    border-radius: 4px;
    &:active {
        box-shadow: 1px 1px 1px 1px black;
    }
`;

const LoginBody = styled.div`
    width: 320px;
    margin: 0 auto;
    color: #2c3e50
`;
const LoginHeader = styled.div`
    font-size: 50px;
    margin-top: 50px;
    margin-bottom: 50px;
    text-align: center;
`;
const LoginText = styled.div`
    text-align: center;
    margin-bottom: 10px;
`;
const handleLoginClick = (e) => {
    e.preventDefault();
    window.location.href = "http://localhost:8001/api/v1/auth/login?next=http://localhost:3000";
};

const LoginPage = () => {
    return (
        <>
            <Header/>
            <LoginBody>
                <LoginHeader>
                    Login
                </LoginHeader>
                <LoginText>
                    Welcome to Automatic Course Picker!
                </LoginText>
                <LoginButton onClick={handleLoginClick}>
                    KAIST SSO Login
                </LoginButton>
            </LoginBody>
        </>
    )
};

export default LoginPage;
