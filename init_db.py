from company_blog import db
from company_blog.models import User

# db.drop_all()
db.create_all()

user1 = User(email="hudnj_siub@geek.com", username="Admin User", password="5tFd72fH", administrator="1")
db.session.add(user1)
db.session.commit()