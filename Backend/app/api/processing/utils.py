import re
import os
import uuid


def parse_article(content):
    pattern = r'\*\*(.+?)\*\*:\s*"(.+?)"'
    matches = re.findall(pattern, content, re.DOTALL)

    article_json = {'Paragraphs': []}
    for key, value in matches:
        if "Paragraph" in key:
            article_json['Paragraphs'].append(value)
        else:
            article_json[key] = value

    return article_json

def DirectoryGenerator(html_content , deployment_directory):

    user_id = str(uuid.uuid4())
    user_output_dir = os.path.join(deployment_directory, user_id)
    os.makedirs(user_output_dir, exist_ok=True)

    with open(os.path.join(user_output_dir, "index.html"), "w") as html_file:
        html_file.write(html_content)

    return user_output_dir


def extract_video_id(url: str) -> str:
    regex_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
        r'(?:https?:\/\/)?youtu\.be\/([^&\s]+)',  
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\s]+)', 
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^&\s]+)'
    ]

    for pattern in regex_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""


def renderBlog(title,question,author,paragraphs):

    paragraphs_html_content = ""
    for paragraph in paragraphs:
            paragraphs_html_content += f'    <p>{paragraph}</p>\n'

    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>{title}</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">

        """ + """
        <style>
                body {
                padding-top:5rem;
            }
            .mainheading {
                padding:1rem 0rem;
            }
            a {
                color:#00ab6b;
            }
            a,a:hover {
                transition:all 0.2s;
            }
            .mediumnavigation {
                background:rgba(255,255,255,.97);
                box-shadow:0 2px 2px -2px rgba(0,0,0,.15);
            }
            section {
                margin-bottom:20px;
            }
            .section-title h2 {
                border-bottom:1px solid rgba(0,0,0,.15);
                margin-bottom:25px;
                font-weight:700;
                font-size:1.4rem;
                margin-bottom:27px;
            }
            .section-title span {
                border-bottom:1px solid rgba(0,0,0,.44);
                display:inline-block;
                padding-bottom:20px;
                margin-bottom:-1px;
            }
            @media (min-width:576px) {
                .card-columns.listfeaturedtag {
                    -webkit-column-count:2;
                    -moz-column-count:2;
                    column-count:2;
                }
            }
            @media (min-width:992px) {
                .navbar-toggleable-md .navbar-nav .nav-link {
                    padding-right:.7rem;
                    padding-left:.7rem;
                }
            }
            .card-columns .card {
                margin-bottom:20px;
            }
            .listfeaturedtag .wrapthumbnail {
                height:258px;
                flex:0 0 auto;
            }
            .listfeaturedtag .card {
                border:1px solid rgba(0,0,0,.1);
                border-radius:2px;
                height:260px;
                padding-left:0;
                margin-bottom:15px;
            }
            .listfeaturedtag .thumbnail {
                background-size:cover;
                height:100%;
                display:block;
                background-origin:border-box!important;
                border-top-left-radius:2px;
            }
            .listfeaturedtag .card-block {
                padding-left:0;
            }
            .listfeaturedtag h2.card-title,.listrecent h2.card-title {
                font-size:1.3rem;
                font-weight:700;
                line-height: 1.25;
            }
            .listfeaturedtag h2.card-title a,.listrecent h2.card-title a {
                color:rgba(0,0,0,.8);
            }
            .listfeaturedtag h2.card-title a:hover,.listrecent h2.card-title a:hover {
                color:rgba(0,0,0,.6);
                text-decoration:none;
            }
            .listfeaturedtag h4.card-text,.listrecent h4.card-text {
                color:rgba(0,0,0,.44);
                font-size:0.95rem;
                line-height:1.4;
                font-weight:400;
            }
            .listfeaturedtag .wrapfooter {
                position:absolute;
                bottom:20px;
                font-size:12px;
                display:block;
                width:85%;
            }
            .listrecent .wrapfooter {
                font-size:12px;
                margin-top:30px;
            }
            .author-thumb {
                width:40px;
                height:40px;
                float:left;
                margin-right:13px;
                border-radius:100%;
            }
            .post-top-meta {
                margin-bottom:2rem;
            }
            .post-top-meta .author-thumb {
                width:72px;
                height:72px;
            }
            .post-top-meta.authorpage .author-thumb {
                margin-top:40px;
            }
            .post-top-meta span {
                font-size:0.9rem;
                color:rgba(0,0,0,.44);
                display:inline-block;
            }
            .post-top-meta .author-description {
                margin-bottom:5px;
                margin-top:5px;
                font-size:0.95rem;
            }
            .author-meta {
                flex:1 1 auto;
                white-space:nowrap!important;
                text-overflow:ellipsis!important;
                overflow:hidden!important;
            }
            span.post-name,span.post-date,span.author-meta {
                display:inline-block;
            }
            span.post-date,span.post-read {
                color:rgba(0,0,0,.44);
            }
            span.post-read-more {
                align-items:center;
                display:inline-block;
                float:right;
                margin-top:8px;
            }
            span.post-read-more a {
                color:rgba(0,0,0,.44);
            }
            span.post-name a,span.post-read-more a:hover {
                color:rgba(0,0,0,.8);
            }
            .dot:after {
                content:"·";
                margin-left:3px;
                margin-right:3px;
            }
            .mediumnavigation .form-control {
                font-size:0.8rem;
                border-radius:30px;
                overflow:hidden;
                border:1px solid rgba(0,0,0,0.04);
            }
            .mediumnavigation .form-inline {
                margin-left:15px;
            }
            .mediumnavigation .form-inline .btn {
                margin-left:-50px;
                border:0;
                border-radius:30px;
                cursor:pointer;
            }
            .mediumnavigation .form-inline .btn:hover,.mediumnavigation .form-inline .btn:active {
                background:transparent;
                color:green;
            }
            .mediumnavigation .navbar-brand {
                font-weight:500;
            }
            .mediumnavigation .dropdown-menu {
                border:1px solid rgba(0,0,0,0.08);
                margin:.5rem 0 0;
            }
            .mediumnavigation .nav-item,.dropdown-menu {
                font-size:0.9rem;
            }
            .mediumnavigation .search-icon {
                margin-left:-40px;
                display:inline-block;
                margin-top:3px;
                cursor:pointer;
            }
            .mediumnavigation .navbar-brand img {
                max-height:30px;
                margin-right:5px;
            }
            .mainheading h1.sitetitle {
                font-family:Righteous;
            }
            .mainheading h1.posttitle {
                font-weight:700;
                margin-bottom:1rem;
            }
            .footer {
                border-top:1px solid rgba(0,0,0,.05)!important;
                padding-top:15px;
                padding-bottom:12px;
                font-size:0.8rem;
                color:rgba(0,0,0,.44);
                margin-top:50px;
            }
            .link-dark {
                color:rgba(0,0,0,.8);
            }
            .article-post {
                font-family:Merriweather;
                font-size:1.2rem;
                line-height:1.8;
                color:rgba(0,0,0,.8);
            }
            blockquote {
                border-left:4px solid #00ab6b;
                padding:0 20px;
                font-style:italic;
                color:rgba(0,0,0,.5);
            }
            .article-post p,.article-post blockquote {
                margin:0 0 1.5rem 0;
            }
            .featured-image {
                display:block;
                margin:0px auto;
                margin-bottom:1.5rem;
            }
            .share {
                text-align:center;
                margin-top:20px;
            }
            .share p {
                margin-bottom:10px;
                font-size:0.95rem;
            }
            .share {
                display:none;
            }
            .share ul li {
                display:inline-block;
                margin-bottom:5px;
            }
            .share ul {
                padding-left:0;
                margin-left:0;
            }
            .svgIcon {
                vertical-align:middle;
            }
            @media (min-width:1024px) {
                .share {
                    position:fixed;
                    display:block;
                }
                .share ul li {
                    display:block;
                }
            }
            @media (max-width:999px) {
                .listfeaturedtag .wrapthumbnail, .listfeaturedtag .col-md-7 {
                    width:100%;
                    max-width:100%;
                    -webkit-box-flex: 0;
                    -webkit-flex: 100%;
                    -ms-flex: 100%;
                    flex: 100%;
                }
                .listfeaturedtag .wrapthumbnail {
                    height:250px;
                }
                .listfeaturedtag .card {
                    height:auto;
                }
                .listfeaturedtag .wrapfooter {
                    position:relative;
                    margin-top:30px;
                }
                .listfeaturedtag .card-block {
                    padding:20px;
                }
            }
            @media (max-width:1024px) {
                .post-top-meta .col-md-10 {
                    text-align:center;
                }
            }
            @media (max-width:767px) {
                .post-top-meta.authorpage {
                    text-align:center;
                }
            }
            .share,.share a {
                color:rgba(0,0,0,.44);
                fill:rgba(0,0,0,.44);
            }
            .graybg {
                background-color:#fafafa;
                padding:40px 0 46px;
                position:relative;
            }
            .listrelated .card {
                box-shadow:0 1px 7px rgba(0,0,0,.05);
                border:0;
            }
            .card {
                border-radius:4px;
            }
            .card .img-thumb {
                border-top-right-radius:4px;
                border-top-left-radius:4px;
            }
            ul.tags {
                list-style:none;
                padding-left:0;
                margin:0 0 3rem 0;
            }
            ul.tags li {
                display:inline-block;
                font-size:0.9rem;
            }
            ul.tags li a {
                background:rgba(0,0,0,.05);
                color:rgba(0,0,0,.6);
                border-radius:3px;
                padding:5px 10px;
            }
            ul.tags li a:hover {
                background:rgba(0,0,0,.07);
                text-decoration:none;
            }
            .margtop3rem {
                margin-top: 3rem;
            }
            .sep {
                height:1px;
                width:20px;
                background:#999;
                margin:0px auto;
                margin-bottom:1.2rem;
            }
            .btn.follow {
                border-color:#02B875;
                color:#1C9963;
                padding:3px 10px;
                text-align:center;
                border-radius:999em;
                font-size:0.85rem;
                display:inline-block;
            }
            .btn.subscribe {
                background-color:#1C9963;
                border-color:#1C9963;
                color:rgba(255,255,255,1);
                fill:rgba(255,255,255,1);
                border-radius:30px;
                font-size:0.85rem;
                margin-left:10px;
                font-weight:600;
                text-transform:uppercase;
            }
            .post-top-meta .btn.follow {
                margin-left:5px;
                margin-top:-4px;
            }
            .alertbar {
                box-shadow:0 -3px 10px 0 rgba(0,0,0,.0785);
                position:fixed;
                bottom:0;
                left:0;
                background-color:#fff;
                width:100%;
                padding:14px 0;
                z-index:1;
            }
            .form-control::-webkit-input-placeholder {
                color: rgba(0,0,0,.5);
            }
            .form-control:-moz-placeholder {
                color: rgba(0,0,0,.5);
            }
            .form-control::-moz-placeholder {
                color: rgba(0,0,0,.5);
            }
            .form-control:-ms-input-placeholder {
                color: rgba(0,0,0,.5);
            }
            .form-control::-ms-input-placeholder {
                color: rgba(0,0,0,.5);
            }
            .authorpage h1 {
                font-weight:700;
                font-size:30px;
            }
            .post-top-meta.authorpage .author-thumb {
                float:none;
            }
            .authorpage .author-description {
                font-size:1rem;
                color:rgba(0,0,0,.6);
            }
            .post-top-meta.authorpage .btn.follow {
                padding:7px 20px;
                margin-top:10px;
                margin-left:0;
                font-size:0.9rem;
            }
            .graybg.authorpage {
                border-top:1px solid #f0f0f0;
            }
            .authorpostbox {
                width:760px;
                margin:0px auto;
                margin-bottom:1.5rem;
                max-width:100%;
            }
            .authorpostbox .img-thumb {
                width:100%;
            }
            .sociallinks {
                margin:1rem 0;
            }
            .sociallinks a {
                background:#666;
                color:#fff;
                width:22px;
                height:22px;
                display:inline-block;
                text-align:center;
                line-height:22px;
                border-radius:50%;
                font-size:12px;
            }

        </style>
        """ + f"""
        
        
        </head>
        <body>


        <nav class="navbar navbar-toggleable-md navbar-light bg-white fixed-top mediumnavigation">
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <div class="container">
            <a class="navbar-brand" href="index.html">
            <p>🪑</p>
            <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item active">
                    <a class="nav-link" href="index.html">Stories <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item">
                    <a class="nav-link" href="post.html">Post</a>
                    </li>
                    <li class="nav-item">
                    <a class="nav-link" href="author.html">Author</a>
                    </li>
                </ul>
                <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="text" placeholder="Search">
                    <span class="search-icon"><svg class="svgIcon-use" width="25" height="25" viewbox="0 0 25 25"><path d="M20.067 18.933l-4.157-4.157a6 6 0 1 0-.884.884l4.157 4.157a.624.624 0 1 0 .884-.884zM6.5 11c0-2.62 2.13-4.75 4.75-4.75S16 8.38 16 11s-2.13 4.75-4.75 4.75S6.5 13.62 6.5 11z"></path></svg></span>
                </form>
            </div>
        </div>
        </nav>
        <div class="container">
            <div class="row">

                <div class="col-md-6 col-md-offset-2 col-xs-12 " style="margin: 0 auto;">
                    <div class="mainheading">

                        <div class="row post-top-meta">
                            <div class="col-md-2">
                                <a href="author.html"><img class="author-thumb" src="https://www.gravatar.com/avatar/e56154546cf4be74e393c62d1ae9f9d4?s=250&amp;d=mm&amp;r=x" alt="Sal"></a>
                            </div>
                            <div class="col-md-10">
                                <a class="link-dark" style="display: block;" href="author.html">{author}</a>
                                <span class="author-description">Creator @ VidJalsa.</span>
                                <span class="post-date">1 1 2030.</span>
                            </div>
                        </div>

                        <h1 class="posttitle"> {title}</h1>
                        <h2 class="question"> {question}</h2>

                    </div>

                    <div class="article-post">
                        {paragraphs_html_content}
                    </div>
                </div>
            </div>
        </div>

        <div class="container">
            <div class="footer">
                <p class="pull-left" style="text-align: center;">
                    Copyright &copy; 2030 VidJalsa
                </p>
                <div class="clearfix">
                </div>
            </div>
        </div>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
        </body>
        </html>
    """ 