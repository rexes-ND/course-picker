import logo from '../statics/Logo_crop_1.png';

const HomePage = (props) => {

    return (
        <div>
            <img src={logo}></img>
            HomePage
            <a href="http://localhost:8001/api/v1/auth/logout?next=http://localhost:3000/login">LOG OUT</a>
        </div>
        
    )
}

export default HomePage