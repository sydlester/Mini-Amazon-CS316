from imaplib import Int2AP
from flask import render_template
from flask_login import current_user
from flask import request
import datetime

from .models.product import Product
from .models.purchase import Purchase

from .models.productReview import ProductReview
from .models.summaryStats import SummaryStats


from flask import Blueprint
bp = Blueprint('productReviewOutput', __name__)


@bp.route('/productReviewOutput/<int:productId>/<int:orderBy>', methods=["GET", "POST"])
def productReviewOutput(productId, orderBy):
    if orderBy == None:
        orderBy = 5
    summary_stats  = SummaryStats.getAvgProductRating(productId)
    product_reviews = ProductReview.get_by_productId(productId, orderBy)
    return render_template('productReviewOutput.html', productId = productId, orderBy = orderBy, product_reviews = product_reviews, summary_stats= summary_stats)
