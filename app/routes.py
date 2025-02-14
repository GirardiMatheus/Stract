from flask import Blueprint, Response, jsonify
from .api import get_platforms, get_accounts, get_fields, get_insights
from .utils import generate_csv, aggregate_data

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return jsonify({
        "name": "Matheus Girardi",
        "email": "girardimatheus27@gmail.com",
        "linkedin": "https://www.linkedin.com/in/matheus-girardi-4857581a8/"
    })

@main_routes.route('/<platform>')
def platform_ads(platform):
    accounts = get_accounts(platform)
    if not accounts or "accounts" not in accounts:
        return jsonify({"error": "No accounts found"}), 404

    all_ads = []
    for account in accounts["accounts"]:
        fields = get_fields(platform)
        if not fields or "fields" not in fields:
            continue

        field_values = ",".join([field["value"] for field in fields["fields"]])
        page = 1
        while True:
            insights = get_insights(platform, account["id"], account["token"], field_values, page)
            if not insights or "insights" not in insights:
                break
            for insight in insights["insights"]:
                insight["account_name"] = account["name"]  
                insight["platform"] = platform  
                all_ads.append(insight)
            if page >= insights.get("pagination", {}).get("total", 1):
                break
            page += 1

    headers = set()
    for ad in all_ads:
        headers.update(ad.keys())
    headers = list(headers)

    return Response(generate_csv(all_ads, headers), mimetype='text/csv')

@main_routes.route('/<platform>/resumo')
def platform_summary(platform):
    accounts = get_accounts(platform)
    if not accounts or "accounts" not in accounts:
        return jsonify({"error": "No accounts found"}), 404

    all_ads = []
    for account in accounts["accounts"]:
        fields = get_fields(platform)
        if not fields or "fields" not in fields:
            continue

        field_values = ",".join([field["value"] for field in fields["fields"]])
        page = 1
        while True:
            insights = get_insights(platform, account["id"], account["token"], field_values, page)
            if not insights or "insights" not in insights:
                break
            for insight in insights["insights"]:
                insight["account_name"] = account["name"]  
                insight["platform"] = platform  
                all_ads.append(insight)
            if page >= insights.get("pagination", {}).get("total", 1):
                break
            page += 1

    numeric_fields = ["clicks", "spend", "impressions", "cpc"]

    aggregated = {}
    for ad in all_ads:
        account_name = ad["account_name"]
        if account_name not in aggregated:
            aggregated[account_name] = {field: 0 for field in numeric_fields}
            aggregated[account_name]["account_name"] = account_name
            aggregated[account_name]["platform"] = platform
        for field in numeric_fields:
            aggregated[account_name][field] += ad.get(field, 0)

    aggregated_data = list(aggregated.values())

    headers = ["platform", "account_name"] + numeric_fields

    return Response(generate_csv(aggregated_data, headers), mimetype='text/csv')

@main_routes.route('/geral')
def geral():
    platforms = get_platforms()
    if not platforms or "platforms" not in platforms:
        return jsonify({"error": "No platforms found"}), 404

    all_ads = []
    all_fields = set()  

    for platform in platforms["platforms"]:
        platform_value = platform["value"]
        accounts = get_accounts(platform_value)
        if not accounts or "accounts" not in accounts:
            continue

        for account in accounts["accounts"]:
            fields = get_fields(platform_value)
            if not fields or "fields" not in fields:
                continue

            field_values = ",".join([field["value"] for field in fields["fields"]])
            page = 1
            while True:
                insights = get_insights(platform_value, account["id"], account["token"], field_values, page)
                if not insights or "insights" not in insights:
                    break
                
                for insight in insights["insights"]:
                    insight["platform"] = platform["text"]
                    insight["account_name"] = account["name"]

                    all_fields.update(insight.keys())

                    all_ads.append(insight)

                if page >= insights.get("pagination", {}).get("total", 1):
                    break
                page += 1

    headers = sorted(all_fields)

    for ad in all_ads:
        for field in headers:
            ad.setdefault(field, "")

    return Response(generate_csv(all_ads, headers), mimetype='text/csv')


@main_routes.route('/geral/resumo')
def geral_resumo():
    platforms = get_platforms()
    if not platforms or "platforms" not in platforms:
        return jsonify({"error": "No platforms found"}), 404

    all_ads = []
    for platform in platforms["platforms"]:
        platform_value = platform["value"]
        accounts = get_accounts(platform_value)
        if not accounts or "accounts" not in accounts:
            continue

        for account in accounts["accounts"]:
            fields = get_fields(platform_value)
            if not fields or "fields" not in fields:
                continue

            field_values = ",".join([field["value"] for field in fields["fields"]])
            page = 1
            while True:
                insights = get_insights(platform_value, account["id"], account["token"], field_values, page)
                if not insights or "insights" not in insights:
                    break
                for insight in insights["insights"]:
                    insight["platform"] = platform["text"]  
                    insight["account_name"] = account["name"] 
                    all_ads.append(insight)
                if page >= insights.get("pagination", {}).get("total", 1):
                    break
                page += 1

    numeric_fields = ["clicks", "spend", "impressions", "cpc"]  
    aggregated = {}
    for ad in all_ads:
        platform = ad["platform"]
        if platform not in aggregated:
            aggregated[platform] = {field: 0 for field in numeric_fields}
            aggregated[platform]["platform"] = platform
        for field in numeric_fields:
            aggregated[platform][field] += ad.get(field, 0)

    aggregated_data = list(aggregated.values())

    headers = ["platform"] + numeric_fields

    return Response(generate_csv(aggregated_data, headers), mimetype='text/csv')
