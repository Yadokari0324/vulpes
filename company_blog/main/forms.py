from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired
from company_blog.models import BlogCategory
from flask_wtf.file import FileField, FileAllowed

class BlogCategoryForm(FlaskForm):
    category = StringField('カテゴリ名', validators=[DataRequired()])
    submit = SubmitField('保存')
    
    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリ名は既に使われています。')
        
class UpdateCategoryForm(FlaskForm):
    category = StringField('カテゴリ名', validators=[DataRequired()])
    submit = SubmitField('更新')
    
    def __init__(self, blog_category_id, *args, **kwargs):
        super(UpdateCategoryForm, self).__init__(*args, **kwargs)
        self.id = blog_category_id
        
    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリ名は既に使われています。')
        
class BlogPostForm(FlaskForm):
    title = StringField('エラー名', validators=[DataRequired()])
    category = SelectField('カテゴリ', coerce=int)
    summary = StringField('教材の章・機能名', validators=[DataRequired()])
    text = TextAreaField('解決法', validators=[DataRequired()])
    picture1 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture2 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture3 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture4 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture5 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture6 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture7 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture8 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture9 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    picture10 = FileField('スクショ', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('投稿')
    
    def _set_category(self):
        blog_categories = BlogCategory.query.all()
        self.category.choices = [(blog_category.id, blog_category.category) for blog_category in blog_categories]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_category()
        
class BlogSearchForm(FlaskForm):
    searchtext = StringField('検索テキスト', validators=[DataRequired()])
    submit = SubmitField('検索')