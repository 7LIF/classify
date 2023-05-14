from typing import List
from decimal import Decimal as dec
from data.models import Item


def latest_items(count: int) -> List[Item]:
    return [
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.215).quantize(dec('0.01')),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = '',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = '',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
    ][:count]
    
    
    
    
    
def popular_items(count: int) -> List[Item]:
    return [
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.215).quantize(dec('0.01')),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = '',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = '',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
    ][:count]
    
    
def random_items(count: int) -> List[Item]:
    return [
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.215).quantize(dec('0.01')),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = '',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = '',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
        Item(
            id = 1,
            post_title = 'Apple Iphone X',
            subcategory = 'Mobile Phones',
            category = 'Mobile Phones',
            publication_date = 'Fev 18, 2023',
            last_update = '1 hours ago',
            price = dec(200.00),
            price_type = 'Fixo',
            item_status = 'Vendido',
            weblink = 'item-details.html',
            location_region = 'Oeiras',
            location_district = 'Lisboa',
            summary =  'Apple Iphone X',
            img_main = 'item_id7_img_main.jpg',
            img1 = '',
            img2 = '',
            img3 = '',
            img4 = '',
            user_id = 7,
            profile_img_url = 'user7.jpg',
            user_name = 'Rui Antunes',
            premium = 'Destacado',
        ),
    ][:count]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""    
                            <div class="col-lg-4 col-md-6 col-12">
                           <!-- Start Single Grid -->
                            <div class="single-grid wow fadeInUp" data-wow-delay=".4s">
                                <div class="image">
                                    <a href="item-details.html" class="thumbnail"><img src="/static/assets/images/items-grid/img2.jpg" alt="#"></a>
                                    <div class="author">
                                        <div class="author-image">
                                            <a href="javascript:void(0)"><img src="/static/assets/images/items-grid/author-2.jpg" alt="#">
                                                <span>Alex Jui</span>
                                            </a>
                                        </div>
                                        <p class="sale">For Sale</p>
                                    </div>
                                </div>
                                <div class="content">
                                    <div class="top-content">
                                        <a href="javascript:void(0)" class="tag">Real Estate</a>
                                        <h3 class="title">
                                            <a href="item-details.html">Amazing Room for Rent</a>
                                        </h3>
                                        <p class="update-time">Last Updated: 2 hours ago</p>
                                        <ul class="rating">
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><a href="javascript:void(0)">(20)</a></li>
                                        </ul>
                                        <ul class="info-list">
                                            <li><a href="javascript:void(0)"><i class="lni lni-map-marker"></i> Dallas, Washington</a></li>
                                            <li><a href="javascript:void(0)"><i class="lni lni-timer"></i> Jan 7, 2023</a></li>
                                        </ul>
                                    </div>
                                    <div class="bottom-content">
                                        <p class="price">Start From: <span>$450.00</span></p>
                                        <a href="javascript:void(0)" class="like"><i class="lni lni-heart"></i></a>
                                    </div>
                                </div>
                            </div>
                            <!--/ End Single Grid -->
                        </div>

                        <div class="col-lg-4 col-md-6 col-12">
                            <!-- Start Single Grid -->
                            <div class="single-grid wow fadeInUp" data-wow-delay=".6s">
                                <div class="image">
                                    <a href="item-details.html" class="thumbnail"><img src="/static/assets/images/items-grid/img3.jpg" alt="#"></a>
                                    <div class="author">
                                        <div class="author-image">
                                            <a href="javascript:void(0)"><img src="/static/assets/images/items-grid/author-3.jpg" alt="#">
                                                <span>Devid Milan</span>
                                            </a>
                                        </div>
                                        <p class="sale">For Sale</p>
                                    </div>
                                    <p class="item-position"><i class="lni lni-bolt"></i> Featured</p>
                                </div>
                                <div class="content">
                                    <div class="top-content">
                                        <a href="javascript:void(0)" class="tag">Mobile Phones</a>
                                        <h3 class="title">
                                            <a href="item-details.html">Canon SX Powershot D-SLR</a>
                                        </h3>
                                        <p class="update-time">Last Updated: 3 hours ago</p>
                                        <ul class="rating">
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><a href="javascript:void(0)">(55)</a></li>
                                        </ul>
                                        <ul class="info-list">
                                            <li><a href="javascript:void(0)"><i class="lni lni-map-marker"></i> New York, US</a></li>
                                            <li><a href="javascript:void(0)"><i class="lni lni-timer"></i> Mar 18, 2023</a></li>
                                        </ul>
                                    </div>
                                    <div class="bottom-content">
                                        <p class="price">Start From: <span>$700.00</span></p>
                                        <a href="javascript:void(0)" class="like"><i class="lni lni-heart"></i></a>
                                    </div>
                                </div>
                            </div>
                            <!--/ End Single Grid -->
                        </div>

                        <div class="col-lg-4 col-md-6 col-12">
                            <!-- Start Single Grid -->
                            <div class="single-grid wow fadeInUp" data-wow-delay=".2s">
                                <div class="image">
                                    <a href="item-details.html" class="thumbnail"><img src="/static/assets/images/items-grid/img4.jpg" alt="#"></a>
                                    <div class="author">
                                        <div class="author-image">
                                            <a href="javascript:void(0)"><img src="/static/assets/images/items-grid/author-4.jpg" alt="#">
                                                <span>Jesia Jully</span>
                                            </a>
                                        </div>
                                        <p class="sale">For Sale</p>
                                    </div>
                                </div>
                                <div class="content">
                                    <div class="top-content">
                                        <a href="javascript:void(0)" class="tag">Vehicles</a>
                                        <h3 class="title">
                                            <a href="item-details.html">BMW 5 Series GT Car</a>
                                        </h3>
                                        <p class="update-time">Last Updated: 4 hours ago</p>
                                        <ul class="rating">
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><a href="javascript:void(0)">(35)</a></li>
                                        </ul>
                                        <ul class="info-list">
                                            <li><a href="javascript:void(0)"><i class="lni lni-map-marker"></i> New York, US</a></li>
                                            <li><a href="javascript:void(0)"><i class="lni lni-timer"></i> Apr 12, 2023</a></li>
                                        </ul>
                                    </div>
                                    <div class="bottom-content">
                                        <p class="price">Start From: <span>$1000.00</span></p>
                                        <a href="javascript:void(0)" class="like"><i class="lni lni-heart"></i></a>
                                    </div>
                                </div>
                            </div>
                            <!--/ End Single Grid -->
                        </div>
                                                                    
                        <div class="col-lg-4 col-md-6 col-12">
                            <!-- Start Single Grid -->
                            <div class="single-grid wow fadeInUp" data-wow-delay=".4s">
                                <div class="image">
                                    <a href="item-details.html" class="thumbnail"><img src="/static/assets/images/items-grid/img5.jpg" alt="#"></a>
                                    <div class="author">
                                        <div class="author-image">
                                            <a href="javascript:void(0)"><img src="/static/assets/images/items-grid/author-5.jpg" alt="#">
                                                <span>Thomas Deco</span>
                                            </a>
                                        </div>
                                        <p class="sale">For Sale</p>
                                    </div>
                                    <p class="item-position"><i class="lni lni-bolt"></i> Featured</p>
                                </div>
                                <div class="content">
                                    <div class="top-content">
                                        <a href="javascript:void(0)" class="tag">Apple</a>
                                        <h3 class="title">
                                            <a href="item-details.html">Apple Macbook Pro 13 Inch</a>
                                        </h3>
                                        <p class="update-time">Last Updated: 5 hours ago</p>
                                        <ul class="rating">
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><a href="javascript:void(0)">(35)</a></li>
                                        </ul>
                                        <ul class="info-list">
                                            <li><a href="javascript:void(0)"><i class="lni lni-map-marker"></i> Louis, Missouri, US</a></li>
                                            <li><a href="javascript:void(0)"><i class="lni lni-timer"></i> May 25, 2023</a></li>
                                        </ul>
                                    </div>
                                    <div class="bottom-content">
                                        <p class="price">Start From: <span>$550.00</span></p>
                                        <a href="javascript:void(0)" class="like"><i class="lni lni-heart"></i></a>
                                    </div>
                                </div>
                            </div>
                            <!--/ End Single Grid -->
                        </div>
                            
                        <div class="col-lg-4 col-md-6 col-12">                                         
                        <!-- Start Single Grid -->
                            <div class="single-grid wow fadeInUp" data-wow-delay=".6s">
                                <div class="image">
                                    <a href="item-details.html" class="thumbnail"><img src="/static/assets/images/items-grid/img6.jpg" alt="#"></a>
                                    <div class="author">
                                        <div class="author-image">
                                            <a href="javascript:void(0)"><img src="/static/assets/images/items-grid/author-6.jpg" alt="#">
                                                <span>Jonson zack</span>
                                            </a>
                                        </div>
                                        <p class="sale">For Sale</p>
                                    </div>
                                </div>

                                <div class="content">
                                    <div class="top-content">
                                        <a href="javascript:void(0)" class="tag">Restaurant</a>
                                        <h3 class="title">
                                            <a href="item-details.html">Cream Restaurant</a>
                                        </h3>
                                        <p class="update-time">Last Updated: 7 hours ago</p>
                                        <ul class="rating">
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><i class="lni lni-star-filled"></i></li>
                                            <li><a href="javascript:void(0)">(20)</a></li>
                                        </ul>
                                        <ul class="info-list">
                                            <li><a href="javascript:void(0)"><i class="lni lni-map-marker"></i> New York, US</a></li>
                                            <li><a href="javascript:void(0)"><i class="lni lni-timer"></i> Feb 18, 2023</a></li>
                                        </ul>
                                    </div>
                                    <div class="bottom-content">
                                        <p class="price">Start From: <span>$500.00</span></p>
                                        <a href="javascript:void(0)" class="like"><i class="lni lni-heart"></i></a>
                                    </div>
                                </div>
                            </div>
                            <!--/ End Single Grid -->
                        </div>
                        
"""



"""
<div class="col-lg-3 col-md-4 col-12">
											<div class="single-item-grid">
												<div class="image">
													<a href="item-details.html"><img
															src="/static/assets/images/items-tab/item-1.jpg" alt="#"></a>
													<i class=" cross-badge lni lni-bolt"></i>
													<span class="flat-badge sale">Sale</span>
												</div>
												<div class="content">
													<a href="javascript:void(0)" class="tag">Mobile</a>
													<h3 class="title">
														<a href="item-details.html">Apple Iphone X</a>
													</h3>
													<p class="location"><a href="javascript:void(0)"><i class="lni
																lni-map-marker">
															</i>Boston</a></p>
													<ul class="info">
														<li class="price">$890.00</li>
														<li class="like"><a href="javascript:void(0)"><i class="lni
																	lni-heart"></i></a>
														</li>
													</ul>
												</div>
											</div>
										</div>


									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-2.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge sale">Sale</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Others</a>
												<h3 class="title">
													<a href="item-details.html">Travel Kit</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>San Francisco</a></p>
												<ul class="info">
													<li class="price">$580.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

									</div>
									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-3.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge sale">Sale</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Electronic</a>
												<h3 class="title">
													<a href="item-details.html">Nikon DSLR Camera</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>Alaska, USA</a></p>
												<ul class="info">
													<li class="price">$560.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

									</div>
									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-4.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge sale">Sale</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Furniture</a>
												<h3 class="title">
													<a href="item-details.html">Poster Paint</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>Las Vegas</a></p>
												<ul class="info">
													<li class="price">$85.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

									</div>
									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-5.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge sale">Sale</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Furniture</a>
												<h3 class="title">
													<a href="item-details.html">Official Metting Chair</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>Alaska, USA</a></p>
												<ul class="info">
													<li class="price">$750.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

									</div>
									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-6.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge rent">Rent</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Books & Magazine</a>
												<h3 class="title">
													<a href="item-details.html">Story Book</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>New York, USA</a></p>
												<ul class="info">
													<li class="price">$120.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

									</div>
									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-7.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge sale">Sale</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Electronic</a>
												<h3 class="title">
													<a href="item-details.html">Cctv camera</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>Delhi, India</a></p>
												<ul class="info">
													<li class="price">$350.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

									</div>
									<div class="col-lg-3 col-md-4 col-12">

										<div class="single-item-grid">
											<div class="image">
												<a href="item-details.html"><img
														src="/static/assets/images/items-tab/item-8.jpg" alt="#"></a>
												<i class=" cross-badge lni lni-bolt"></i>
												<span class="flat-badge sale">Sale</span>
											</div>
											<div class="content">
												<a href="javascript:void(0)" class="tag">Mobile</a>
												<h3 class="title">
													<a href="item-details.html">Samsung Glalaxy S8</a>
												</h3>
												<p class="location"><a href="javascript:void(0)"><i class="lni
															lni-map-marker">
														</i>Delaware, USA</a></p>
												<ul class="info">
													<li class="price">$299.00</li>
													<li class="like"><a href="javascript:void(0)"><i class="lni
																lni-heart"></i></a>
													</li>
												</ul>
											</div>
										</div>

"""