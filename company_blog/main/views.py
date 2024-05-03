from flask import Blueprint, render_template, request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from company_blog.models import BlogCategory, BlogPost
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm, BlogPostForm, BlogSearchForm
from company_blog import db
from company_blog.main.image_handler import add_featured_image

from flask import Flask, render_template, request

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

main = Blueprint('main', __name__)

@main.route('/category_maintenance', methods=['GET', 'POST'])
@login_required
def category_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).paginate(page=page, per_page=10)
    form = BlogCategoryForm()
    if form.validate_on_submit():
        blog_category = BlogCategory(category=form.category.data)
        db.session.add(blog_category)
        db.session.commit()
        flash('ブログカテゴリが追加されました')
        return redirect(url_for('main.category_maintenance'))
    elif form.errors:
        form.category.data = ""
        flash(form.errors['category'][0])
    return render_template('category_maintenance.html', blog_categories=blog_categories, form=form)

@main.route('/<int:blog_category_id>/blog_category', methods=['GET', 'POST'])
@login_required
def blog_category(blog_category_id):
    if not current_user.is_administrator():
        abort(403)
    blog_category = BlogCategory.query.get_or_404(blog_category_id)
    form = UpdateCategoryForm(blog_category_id)
    if form.validate_on_submit():
        blog_category.category = form.category.data
        db.session.commit()
        flash('ブログカテゴリが更新されました')
        return redirect(url_for('main.category_maintenance'))
    elif request.method == 'GET':
        form.category.data = blog_category.category
    return render_template('blog_category.html', form=form)

@main.route('/<int:blog_category_id>/delete_category', methods=['GET', 'POST'])
@login_required
def delete_category(blog_category_id):
    if not current_user.is_administrator():
        abort(403)
    blog_category = BlogCategory.query.get_or_404(blog_category_id)
    db.session.delete(blog_category)
    db.session.commit()
    flash('ブログカテゴリが削除されました')
    return redirect(url_for('main.category_maintenance'))

@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        # if form.picture1.data:
        #     pic1 = add_featured_image(form.picture1.data)
        # else:
        #     pic1 = ''
        # if form.picture2.data:
        #     pic2 = add_featured_image(form.picture2.data)
        # else:
        #     pic2 = ''
        # if form.picture3.data:
        #     pic3 = add_featured_image(form.picture3.data)
        # else:
        #     pic3 = ''
        # if form.picture4.data:
        #     pic4 = add_featured_image(form.picture4.data)
        # else:
        #     pic4 = ''
        # if form.picture5.data:
        #     pic5 = add_featured_image(form.picture5.data)
        # else:
        #     pic5 = ''
        # if form.picture6.data:
        #     pic6 = add_featured_image(form.picture6.data)
        # else:
        #     pic6 = ''
        # if form.picture7.data:
        #     pic7 = add_featured_image(form.picture7.data)
        # else:
        #     pic7 = ''
        # if form.picture8.data:
        #     pic8 = add_featured_image(form.picture8.data)
        # else:
        #     pic8 = ''
        # if form.picture9.data:
        #     pic9 = add_featured_image(form.picture9.data)
        # else:
        #     pic9 = ''
        # if form.picture10.data:
        #     pic10 = add_featured_image(form.picture10.data)
        # else:
        #     pic10 = ''
        blog_post = BlogPost(title=form.title.data, text=form.text.data, featured_image1=form.picture1.data, featured_image2=form.picture2.data, featured_image3=form.picture3.data, featured_image4=form.picture4.data, featured_image5=form.picture5.data, featured_image6=form.picture6.data, featured_image7=form.picture7.data, featured_image8=form.picture8.data, featured_image9=form.picture9.data, featured_image10=form.picture10.data, user_id=current_user.id, category_id=form.category.data, summary=form.summary.data)
        db.session.add(blog_post)
        db.session.commit()
        flash('ブログ投稿が作成されました')
        return redirect(url_for('main.blog_maintenance'))
    return render_template('create_post.html', form=form)

@main.route('/blog_maintenance')
@login_required
def blog_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
    return render_template('blog_maintenance.html', blog_posts=blog_posts)

@main.route('/<int:blog_post_id>/blog_post')
def blog_post(blog_post_id):
    form = BlogSearchForm()
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()
    
    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    return render_template('blog_post.html', post=blog_post, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)

@main.route('/<int:blog_post_id>/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('ブログ投稿が削除されました')
    return redirect(url_for('main.blog_maintenance'))

@main.route('/<int:blog_post_id>/update_post', methods=['GET', 'POST'])
@login_required
def update_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        # if form.picture1.data:
        #     blog_post.featured_image1 = add_featured_image(form.picture1.data)
        # if form.picture2.data:
        #     blog_post.featured_image2 = add_featured_image(form.picture2.data)
        # if form.picture3.data:
        #     blog_post.featured_image3 = add_featured_image(form.picture3.data)
        # if form.picture4.data:
        #     blog_post.featured_image4 = add_featured_image(form.picture4.data)
        # if form.picture5.data:
        #     blog_post.featured_image5 = add_featured_image(form.picture5.data)
        # if form.picture6.data:
        #     blog_post.featured_image6 = add_featured_image(form.picture6.data)
        # if form.picture7.data:
        #     blog_post.featured_image7 = add_featured_image(form.picture7.data)
        # if form.picture8.data:
        #     blog_post.featured_image8 = add_featured_image(form.picture8.data)
        # if form.picture9.data:
        #     blog_post.featured_image9 = add_featured_image(form.picture9.data)
        # if form.picture10.data:
        #     blog_post.featured_image10 = add_featured_image(form.picture10.data)
        blog_post.featured_image1 = form.picture1.data
        blog_post.featured_image2 = form.picture2.data
        blog_post.featured_image3 = form.picture3.data
        blog_post.featured_image4 = form.picture4.data
        blog_post.featured_image5 = form.picture5.data
        blog_post.featured_image6 = form.picture6.data
        blog_post.featured_image7 = form.picture7.data
        blog_post.featured_image8 = form.picture8.data
        blog_post.featured_image9 = form.picture9.data
        blog_post.featured_image10 = form.picture10.data
        blog_post.text = form.text.data
        blog_post.summary = form.summary.data
        blog_post.category_id = form.category.data
        db.session.commit()
        flash('ブログ投稿が更新されました')
        return redirect(url_for('main.blog_post', blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.picture1.data = blog_post.featured_image1
        form.picture2.data = blog_post.featured_image2
        form.picture3.data = blog_post.featured_image3
        form.picture4.data = blog_post.featured_image4
        form.picture5.data = blog_post.featured_image5
        form.picture6.data = blog_post.featured_image6
        form.picture7.data = blog_post.featured_image7
        form.picture8.data = blog_post.featured_image8
        form.picture9.data = blog_post.featured_image9
        form.picture10.data = blog_post.featured_image10
        form.text.data = blog_post.text
        form.summary.data = blog_post.summary
        form.category.data = blog_post.category_id
    return render_template('create_post.html', form=form)

@main.route('/')
@login_required
def index():
    form = BlogSearchForm()
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
    
    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()
    
    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    
    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = BlogSearchForm()
    searchtext = ""
    if form.validate_on_submit():
        searchtext = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data = ""
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter((BlogPost.text.contains(searchtext)) | (BlogPost.title.contains(searchtext)) | (BlogPost.summary.contains(searchtext))).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
    
    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()
    
    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    
    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form, searchtext=searchtext)

@main.route('/<int:blog_category_id>/category_posts')
def category_posts(blog_category_id):
    form = BlogSearchForm()
    
    # カテゴリ名の取得
    blog_category = BlogCategory.query.filter_by(id=blog_category_id).first_or_404()
    
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(category_id=blog_category_id).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
    
    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()
    
    # カテゴリの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()
    
    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, blog_category=blog_category, form=form)


@main.route("/zemi")
def zemi():
    return render_template("zemi.html")

# predictページにはGETメソッドとPOSTメソッドの二通りのアクセスの仕方があります。
# その時にはmethodsを準備しておく必要がありましたね。
@main.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")
    elif request.method == "POST":
        quote2 = request.form["name2"]
        quote3 = request.form["name3"]
        quote4 = request.form["name4"]
        quote5 = request.form["name5"]
        quote6 = request.form["name6"]
        # result = predict_sentiment(quote)
        data = {
            'id': [100],
            'function': 'a',
            'design_role_model': [quote2],
            'design_html': [quote3],
            'design_css_position': [quote4],
            'design_css_color': [quote5],
            'error': [quote6],
            'release': 'a',
            'image_url': 'a',
            'link_url': 'a',
            'name': 'a',
            'explanatory_text': 'a',
        }
        # label = result[0]["label"]
        # score = round(result[0]["score"], 3)
        # render_templateで引数を渡す方法を確認しましょう。
        df2 = pd.DataFrame(data)
        df2 = df2.set_index('id')
        df1 = pd.read_csv("book3.csv", index_col=0)
        
        
        cos_list = []
        for user_id in df1.index:
            cos_list.append(cosine_similarity([df2.loc[100, ["design_role_model", "design_html", "design_css_position", "design_css_color", "error"]]], [df1.loc[user_id, ["design_role_model", "design_html", "design_css_position", "design_css_color", "error"]]]))
        df3 = pd.DataFrame([cos_list])
        df4 = df3.T
        df4.index = df4.index + 1


        # DataFrameを水平に連結する
        result = pd.concat([df1, df4], axis=1)
        result['Index_Column'] = result.index

        # カラム0のリストから数値を取り出す
        # df4['0'] = df4['0'].apply(lambda x: x[0])

        # カラム0で降順にソート
        df_sorted = result.sort_values(0, ascending=False)

        age_list = df_sorted['Index_Column'].tolist()
        age_list2 = df_sorted['link_url'].tolist()
        age_list3 = df_sorted['explanatory_text'].tolist()
        age_list4 = df_sorted['name'].tolist()
        
        first_one = age_list[:1]
        next_two = age_list[1:3]
        next_three = age_list[3:7]
        rest = age_list[7:]
        
        first_one2 = age_list2[:1]
        next_two2 = age_list2[1:3]
        next_three2 = age_list2[3:7]
        rest2 = age_list2[7:]
        
        first_one3 = age_list3[:1]
        next_two3 = age_list3[1:3]
        next_three3 = age_list3[3:7]
        rest3 = age_list3[7:]
        
        first_one4 = age_list4[:1]
        next_two4 = age_list4[1:3]
        next_three4 = age_list4[3:7]
        rest4 = age_list4[7:]
        
        return render_template(
            "predict.html",
            df_sorted = df_sorted,
            age_list = age_list,
            I = zip(first_one, first_one2, first_one3, first_one4),
            II = zip(next_two, next_two2, next_two3, next_two4),
            III = zip(next_three, next_three2, next_three3, next_three4),
            IIII = zip(rest, rest2, rest3, rest4),
            # first_one = first_one,
            # next_two = next_two,
            # next_three = next_three,
            # rest = rest,
            # first_one2 = first_one2,
            # next_two2 = next_two2,
            # next_three2 = next_three2,
            # rest2 = rest2,
        )