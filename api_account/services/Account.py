from api_base.services import CloudinaryService


class AccountService:

    @classmethod
    def upload_avatar(cls, image):
        upload_data = CloudinaryService.upload_avatar_user_image(image)
        return upload_data.get("url")
