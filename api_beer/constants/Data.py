from enum import Enum


class ProducerMigration(Enum):
    HEINEKEN = {
        "id": "217e5e68754046218c617b2d33cdc6ae",
        "name": "Heineken",
        "company_name": "Heineken N.V.",
        "address": "Đường số 6, KCN Hòa Khánh, Phường Hòa Khánh Bắc, Liên Chiểu, Đà Nẵng, Việt Nam"
    }
    BUDWEISER = {
        "id": "4478103bd22f4955a16281ad5b15ed28",
        "name": "Budweiser",
        "company_name": "Anheuser-Busch Inbev",
        "address": "86 Ngô Thế Vinh, Hòa Cường, Hải Châu, Đà Nẵng, Việt Nam"
    }
    SAPPORO = {
        "id": "f69b1ebf58e0498a9431c67e62091282",
        "name": "Sapporo",
        "company_name": "Sapporo Breweries",
        "address": "Đường Cây Keo, Tam Phú, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam"
    }
    CORONA = {
        "id": "c29737f712574d448088562439c12abb",
        "name": "Corona",
        "company_name": "Cerveceria Modelo",
        "address": "52 Đường 2, Bình Chiểu, Thủ Đức, Bình Dương, Việt Nam"
    }
    HUDA = {
        "id": "d0bb60155fa540828010ddc0775f1d66",
        "name": "Huda",
        "company_name": "Carlsberg",
        "address": "Trường Sơn, Phường 2, Tân Bình, Thành phố Hồ Chí Minh, Việt Nam"
    }
    LEFFE = {
        "id": "82b6edb0902a433cbffcb7f27c43482b",
        "name": "Leffe",
        "company_name": "Anheuser-Busch Inbev",
        "address": "360 Phạm Hùng, Hoà Phước, Hòa Vang, Đà Nẵng"
    }
    STRONGBOW = {
        "id": "d28ce6c61c7049e3a3f7a4bd2a3a9e27",
        "name": "Strongbow",
        "company_name": "Scottish & Newcastle",
        "address": "29A Ngõ 124 Phố Vĩnh Tuy, Thanh Long, Hai Bà Trưng, Hà Nội, Việt Nam"
    }


class NationMigration(Enum):
    VIETNAM = {
        "id": "e478bebde2f64da6a9c1bd302a3fb698",
        "name": "Việt Nam",
        "flag_picture": "https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638012/SGroup/KOB/nations/vietnam_1_wftv2l.png"
    }
    MEXICO = {
        "id": "0e8e3e3254f343b883abae3219f13fd6",
        "name": "Mexico",
        "flag_picture": "https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638121/SGroup/KOB/nations/mexico_jnwrnn.png"
    }
    SINGAPORE = {
        "id": "de448c2246ed4093a438c8913f0afe7d",
        "name": "Singapore",
        "flag_picture": "https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638083/SGroup/KOB/nations/singapore_va8ebk.png"
    }
    FRANCE = {
        "id": "792d5566131e4d9f80269eae5eb502df",
        "name": "France",
        "flag_picture": "https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638055/SGroup/KOB/nations/france_k2kht3.png"
    }
    AMERICA = {
        "id": "3d76ecf37e5a4a94a04748eaf7c160c5",
        "name": "America",
        "flag_picture": "https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638034/SGroup/KOB/nations/united-states_imyw4u.png"
    }
    NETHERLANDS = {
        "id": "d92bb7d65fc441488e0affa85eb97ed3",
        "name": "Hà Lan",
        "flag_picture": "https://res.cloudinary.com/ddqzgiilu/image/upload/v1638638899/SGroup/KOB/nations/netherlands_aafwe0.png"
    }
