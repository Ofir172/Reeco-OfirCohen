import requests
import pandas as pd
import csv
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

# GraphQL endpoint and headers
url = "https://gateway-api.shop.sysco.com/graphql"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "SYY-Authorization": os.getenv("SYY_AUTH"),
    "User-Agent": os.getenv("USER_AGENT"),
    "Authorization": os.getenv("AUTHORIZATION"),
    "Cookie": os.getenv("COOKIE"),
    "Referer": "https://shop.sysco.com/",
}

# GraphQL queries
query_category = "fragment FacetValueFields on SearchResultFacetValue {\n  id\n  name\n  records\n}\n\nquery SearchProducts($params: ProductSearchQuery!, $isBestSellerEnabled: Boolean = false, $isUseGraphStockStatusEnabled: Boolean = false, $isRebatesPhase2Enabled: Boolean = false, $isGuest: Boolean = false) {\n  searchProducts(params: $params) {\n    metaInfo {\n      originalQuery {\n        q\n        start\n        num\n        facetSize\n        facets {\n          id\n          value\n        }\n        sort\n      }\n      correlationId\n      responseTimeInMills\n      totalResults\n      searchTemplateName\n      queryId\n      searchId\n      algorithmType\n      autoCorrect\n      originalSearchTermType\n      executedSort\n    }\n    facets {\n      id\n      values {\n        ...FacetValueFields\n        values {\n          ...FacetValueFields\n          values {\n            ...FacetValueFields\n          }\n        }\n      }\n    }\n    results {\n      sellerId\n      siteId\n      isBestSeller @include(if: $isBestSellerEnabled)\n      productId\n      availableStockInfo {\n        inventory {\n          nextReceiveQuantity\n          quantityOnHand\n          unitOfMeasure\n          availableOnHand\n          stockStatus @include(if: $isUseGraphStockStatusEnabled)\n        }\n        nextReceiveDate\n        stockIndicator\n        unitsPerCase\n      }\n      seller {\n        id\n        name\n        group\n        provider\n      }\n      productInfo {\n        constraints {\n          quantity {\n            incrementalOrderQuantity\n            minimumOrderQuantity\n            soldAs\n          }\n        }\n        isOpot\n        name\n        description\n        brand {\n          id\n          name\n        }\n        category {\n          mainId\n          mainName\n          majorId\n          intermediateId\n          intermediateName\n          minorId\n          minorName\n          majorName\n          name\n          displayName\n          complete\n        }\n        packSize {\n          pack\n          size\n          uom\n        }\n        isSoldAs {\n          split\n          case\n        }\n        split {\n          min\n          max\n        }\n        averageWeightPerCase\n        stockType\n        isCatchWeight\n        isSyscoBrand\n        isPhasedOut\n        isExpandedAssortment\n        images\n        isOrderable\n        gpo {\n          iconGroup\n          indicatorNo\n          name\n          value\n          font\n          size\n          style\n          color\n          width\n          height\n          positionX\n          positionY\n          description\n        }\n        isLeavingSoon\n        sourceVendor\n        demandStatusFlag\n        specialist {\n          id\n          name\n        }\n        broker {\n          name\n          id\n        }\n        weightUom\n        stockTypeCode\n        isShopOrderable\n        replacementProduct {\n          sellerId\n          siteId\n          productId\n        }\n        storageFlag\n      }\n      shippingTimeEstimation {\n        cs {\n          earliest\n          latest\n          shippingTimeUom\n        }\n        ea {\n          earliest\n          latest\n          shippingTimeUom\n        }\n      }\n      rebateInfo @include(if: $isRebatesPhase2Enabled) {\n        isSyscoBrandEligible\n      }\n      productListInfo @skip(if: $isGuest) {\n        isFavorite\n        favoritesFetched\n      }\n      purchaseHistoryInfo {\n        orderedDate\n        orderQuantity\n      }\n    }\n  }\n}\n"

query_product = "query getProducts_details_unifiedBFF_SHOP_WEB($products: ProductQuery!, $productRelationships: [RelationshipType!], $isBestSellerEnabled: Boolean = false, $isGuest: Boolean = false, $isPriceInfo: Boolean = false, $isPriceInfoV2: Boolean = false, $isRebatesPhase2Enabled: Boolean = false, $isBuyAmericanEnabled: Boolean = false) {\n  getProducts(products: $products, productRelationships: $productRelationships) {\n    sellerId\n    siteId\n    productId\n    isBestSeller @include(if: $isBestSellerEnabled)\n    rePurchaseRateInfo @skip(if: $isGuest) {\n      rePurchasePercentage\n      rePurchaseCount\n      purchaseCount\n    }\n    productInfo {\n      constraints {\n        quantity {\n          soldAs\n          minimumOrderQuantity\n          incrementalOrderQuantity\n        }\n      }\n      isBuyAmerican @include(if: $isBuyAmericanEnabled)\n      regulatedCertificates @include(if: $isBuyAmericanEnabled) {\n        name\n        source\n        type\n        url\n      }\n      servingsPerCase\n      assortmentClassification {\n        type\n        color\n        priority\n      }\n      rewardPoints\n      averageWeightPerCase\n      brand {\n        id\n        name\n      }\n      broker {\n        number\n        name\n        contactName\n        contactPhone\n        contactEmail\n        id\n      }\n      category {\n        mainId\n        mainName\n        majorId\n        intermediateId\n        intermediateName\n        minorId\n        minorName\n        majorName\n        name\n        displayName\n        complete\n      }\n      description\n      demandStatusFlag\n      featuresAndBenefits {\n        productDescriptor\n        packagingInformation\n        sizeAndShapeOfProduct\n        yieldOrServingSize\n        qualityAndFormat\n        prepCookingInstructions\n        storageAndUsage\n        handlingInstructions\n        additionalProductInformation\n        marketingStatements\n        culinaryApplications\n      }\n      gtin\n      grossWeight\n      images\n      isAvailable\n      isCatchWeight\n      isDropShip\n      isOrderable\n      isOpot\n      isPhasedOut\n      isSyscoBrand\n      isShipSplitOnly\n      isShopOrderable\n      isSoldAs {\n        split\n        case\n      }\n      lineDescription\n      localDescription\n      manufacturerUPC\n      name\n      netWeight\n      packSize {\n        pack\n        size\n        uom\n      }\n      replacementProduct {\n        productId\n      }\n      sourceVendor\n      sourceVendorType\n      sourceVendorShipPtNumber\n      specialist {\n        name\n        phone\n      }\n      split {\n        min\n        max\n      }\n      stockType\n      unitPerCase\n      weightUom\n      consumerInformation {\n        generalDescription\n        prepAndCookingInstructions\n        storageAndUsage\n        servingSuggestions\n      }\n      dimension {\n        uom\n        length\n        width\n        height\n      }\n      totalShelfLife\n      trueVendorName\n      statusCode\n      storageFlag\n      taxonomy {\n        hierarchyId\n        businessCenter\n        itemGroup\n        attributeGroup\n        attributes\n        taxonomyAttributes {\n          value\n          priority\n          name\n        }\n        businessCenterId\n        itemGroupId\n        attributeGroupId\n      }\n      isExpandedAssortment\n      siteRelatedProducts {\n        productId\n        relationshipType\n      }\n      supplyAvailability {\n        isSupplyDisrupted\n        disruptionStartDate\n        disruptionEndDate\n      }\n      sustainabilityAttributes {\n        displayText\n      }\n      gpo {\n        indicatorNo\n        description\n        contractId\n        contractStartDate\n        contractEndDate\n      }\n      uuom {\n        uomName\n        uomQuantity\n        equivalentUomQuantity\n        usageLot\n        universalUomName\n        ruleUsed\n      }\n    }\n    shippingTimeEstimation {\n      cs {\n        earliest\n        latest\n        shippingTimeUom\n      }\n      ea {\n        earliest\n        latest\n        shippingTimeUom\n      }\n    }\n    priceInfo @include(if: $isPriceInfo) {\n      case {\n        ...caseEachPrices\n      }\n      each {\n        ...caseEachPrices\n      }\n    }\n    priceInfoV2 @include(if: $isPriceInfoV2) {\n      case(products: $products) {\n        ...caseEachPricesV2\n      }\n      each(products: $products) {\n        ...caseEachPricesV2\n      }\n    }\n    rebateInfo @include(if: $isRebatesPhase2Enabled) {\n      isSyscoBrandEligible\n    }\n    purchaseHistoryInfo @skip(if: $isGuest) {\n      orderedDate\n      orderQuantity\n      splitCode\n    }\n    productListInfo @skip(if: $isGuest) {\n      isFavorite\n      favoritesFetched\n    }\n    seller {\n      id\n      name\n      provider\n      group\n    }\n  }\n}\n\nfragment caseEachPrices on PricingInformation {\n  pricingExtn {\n    leadTimeToShip\n    earliestDeliveryDate\n    latestDeliveryDate\n  }\n  priceZoneId\n  quantity\n  grossPrice\n  customerReferencePrice\n  orderPrice\n  unitPrice\n  netPrice\n  agreementIndicators\n  agreements {\n    effectiveTo\n    effectiveFrom\n    methodCode\n    priceAdjustmentCode\n    priceAdjustment\n    description\n    applicationCode\n    type\n    id\n  }\n  exception {\n    id\n    price\n    effectiveFrom\n    effectiveTo\n  }\n  discounts {\n    amountType\n    priceAdjustment\n    name\n    type\n    id\n    amount\n    effectiveFrom\n    effectiveTo\n    promoId\n  }\n  volumePricingTiers {\n    customerPrequalifiedPrice\n    unitPrice\n    netPrice\n    discounts {\n      id\n      type\n      name\n      priceAdjustment\n      amountType\n      amount\n      effectiveFrom\n      effectiveTo\n    }\n    agreements {\n      id\n      type\n      applicationCode\n      priceAdjustment\n      description\n      priceAdjustmentCode\n      rebateBasis\n      methodCode\n      effectiveFrom\n      effectiveTo\n    }\n    eligibility {\n      operator\n      lowerBound\n      upperBound\n    }\n  }\n  lastPrice\n  lastMargin\n  unitCommissionBasis\n  minHandlingFlag\n  maxHandlingFlag\n  handPricingAllowedFlag\n  handPricing {\n    minPrice\n    maxPrice\n  }\n  price\n  minPrice\n  maxPrice\n}\n\nfragment caseEachPricesV2 on PricingInformationV2 {\n  pricingExtn {\n    leadTimeToShip\n    earliestDeliveryDate\n    latestDeliveryDate\n  }\n  priceZoneId\n  quantity\n  grossPrice\n  customerReferencePrice\n  orderPrice\n  unitPrice\n  netPrice\n  agreementIndicators\n  agreements {\n    effectiveTo\n    effectiveFrom\n    methodCode\n    priceAdjustmentCode\n    priceAdjustment\n    description\n    applicationCode\n    type\n    id\n  }\n  exception {\n    id\n    price\n    effectiveFrom\n    effectiveTo\n  }\n  discounts {\n    amountType\n    priceAdjustment\n    name\n    type\n    id\n    amount\n    effectiveFrom\n    effectiveTo\n    promoId\n  }\n  volumePricingTiers {\n    customerPrequalifiedPrice\n    unitPrice\n    netPrice\n    discounts {\n      id\n      type\n      name\n      priceAdjustment\n      amountType\n      amount\n      effectiveFrom\n      effectiveTo\n    }\n    agreements {\n      id\n      type\n      applicationCode\n      priceAdjustment\n      description\n      priceAdjustmentCode\n      rebateBasis\n      methodCode\n      effectiveFrom\n      effectiveTo\n    }\n    eligibility {\n      operator\n      lowerBound\n      upperBound\n    }\n  }\n  lastPrice\n  lastMargin\n  unitCommissionBasis\n  minHandlingFlag\n  maxHandlingFlag\n  handPricingAllowedFlag\n  handPricing {\n    minPrice\n    maxPrice\n  }\n  price\n  minPrice\n  maxPrice\n  rebateValue\n}\n"

# Identify and prepare all categories for scraping
def get_categories():
    variables_facets = {
        "isBestSellerEnabled": False,
        "isUseGraphStockStatusEnabled": True,
        "isRebatesPhase2Enabled": False,
        "isGuest": True,
        "params": {
            "facets": [
                {"id": "STOCK_TYPE", "value": "S"}
            ],
            "sort": {"type": "BEST_MATCH", "order": "DESC"},
            "pageName": "CATALOG",
            "start": 0,
            "num": 1
        }
    }

    payload_facets = {
        "operationName": "SearchProducts",
        "query": query_category,
        "variables": variables_facets
    }

    response = requests.post(url, json=payload_facets, headers=headers)
    facets_data = response.json()["data"]["searchProducts"]["facets"]

    # Find the specific facet containing category taxonomy
    category_facet = None
    for f in facets_data:
        if f.get("id") == "SYSCO_6":
            category_facet = f
            break

    # Build a list of category IDs and names for scraping
    categories = []
    for cat in category_facet["values"]:
        if cat["id"].startswith("syy_cust_tax_"):
            categories.append((cat["id"], cat["name"]))

    return categories

# Async function to fetch and parse product details by product ID
async def fetch_product_details(session, product_id, category_name):
    payload_product = {
        "operationName": "getProducts_details_unifiedBFF_SHOP_WEB",
        "query": query_product,
        "variables": {
            "isBestSellerEnabled": False,
            "isGuest": True,
            "isPriceInfo": False,
            "isPriceInfoV2": False,
            "isRebatesPhase2Enabled": False,
            "isBuyAmericanEnabled": True,
            "products": {
                "params": [
                    {
                        "sellerId": "USBL",
                        "productId": product_id,
                        "siteId": "052"
                    }
                ]
            },
            "productRelationships": ["C"]
        }
    }

    try:
        async with session.post(url, json=payload_product, headers=headers) as resp:
            if resp.status != 200:
                print(f"Error fetching product {product_id}")
                return None

            data_product = await resp.json()
            product = data_product["data"]["getProducts"][0]

            # Parse product fields
            brand_name = product.get("productInfo", {}).get("brand", {}).get("name", "").title()
            product_name = str(product.get("productInfo", {}).get("description", ""))
            pack = product.get("productInfo", {}).get("packSize", {}).get("pack") or ""
            size = product.get("productInfo", {}).get("packSize", {}).get("size") or ""
            packaging = f"{pack}/{size}".strip("/")
            sku = product.get("productId", "")
            images = product.get("productInfo", {}).get("images", [])
            picture_url = images[0] if images else None
            description = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("productDescriptor", ""))
            packagingInformation = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("packagingInformation", ""))
            sizeAndShape = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("sizeAndShapeOfProduct", ""))
            yieldOrServingSize = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("yieldOrServingSize", ""))
            qualityAndFormat = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("qualityAndFormat", ""))
            prepAndCookingInstructions = str(product.get("productInfo", {}).get("consumerInformation", {}).get("prepAndCookingInstructions", ""))
            storageAndUsage = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("storageAndUsage", ""))
            handlingInstructions = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("handlingInstructions", ""))
            additionalInformation = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("additionalProductInformation", ""))
            culinaryApplications = str(product.get("productInfo", {}).get("featuresAndBenefits", {}).get("culinaryApplications", ""))
            gtin = str(product.get("productInfo", {}).get("gtin", ""))
            manufacturerUPC = str(product.get("productInfo", {}).get("manufacturerUPC", ""))
            netWeight = str(product.get("productInfo", {}).get("netWeight", ""))

            return {
                "Brand Name": brand_name,
                "Product Name": product_name,
                "Packaging": packaging,
                "SKU (Product ID)": sku,
                "Picture URL": picture_url,
                "Description": description,
                "Category": category_name,
                "Packaging Information": packagingInformation,
                "Size And Shape": sizeAndShape,
                "Yield Or Serving Size": yieldOrServingSize,
                "Quality And Format": qualityAndFormat,
                "Prep And Cooking Instructions": prepAndCookingInstructions,
                "Storage And Usage": storageAndUsage,
                "handling Instructions": handlingInstructions,
                "Additional Information": additionalInformation,
                "Culinary Applications": culinaryApplications,
                "GTIN": gtin,
                "Manufacturer UPC": manufacturerUPC,
                "Net Weight": netWeight

            }

    except Exception as e:
        print(f"Exception for product {product_id}: {e}")
        return None

# Loop over each category and fetch all products using pagination
def process_category(category_id, category_name, writer, include_header):
    start = 0
    num = 24
    total_results = None
    product_counter = 0
    page_counter = 1

    while True:
        # Construct GraphQL payload for current category page
        variables_category = {
            "isBestSellerEnabled": False,
            "isUseGraphStockStatusEnabled": True,
            "isRebatesPhase2Enabled": False,
            "isGuest": True,
            "params": {
                "facets": [
                    {"id": "BUSINESS_CENTER_ID", "value": category_id, "size": 1000},
                    {"id": "STOCK_TYPE", "value": "S"}
                ],
                "sort": {"type": "BEST_MATCH", "order": "DESC"},
                "pageName": "CATALOG",
                "start": start,
                "num": num
            }
        }

        payload_category = {
            "operationName": "SearchProducts",
            "query": query_category,
            "variables": variables_category
        }

        # Fetch current page of products in category
        response_category = requests.post(url, json=payload_category, headers=headers)
        if response_category.status_code != 200:
            print(f"Error fetching category {category_name} (start={start})")
            break

        data_category = response_category.json()
        products_raw = data_category["data"]["searchProducts"]["results"]
        product_ids = [p["productId"] for p in products_raw]

        # Launch all product detail requests concurrently for current page
        async def process_products():
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_product_details(session, pid, category_name) for pid in product_ids]
                results = await asyncio.gather(*tasks)
                return [r for r in results if r is not None]

        all_products = asyncio.run(process_products())
        product_counter += len(all_products)
        if all_products:
            df = pd.DataFrame(all_products)
            df.to_csv("allproducts.csv", mode="a", index=False, encoding="utf-8-sig", header=False)
            include_header = False  # write header only once

        if total_results is None:
            total_results = data_category["data"]["searchProducts"]["metaInfo"]["totalResults"]
            print(f"Total products in {category_name}: {total_results}")

        print(f"Processed page {page_counter} in {category_name} ({product_counter} products total so far)")
        start += num
        page_counter += 1
        if start >= total_results:
            break

    print(f"Finished category: {category_name} — {product_counter} products")

# Initialize the CSV file and write column headers
def scrape_all_products():
    categories = get_categories()
    fieldnames = [
        "Brand Name", "Product Name", "Packaging",
        "SKU (Product ID)", "Picture URL", "Description", "Category",
        "Packaging Information", "Size And Shape", "Yield Or Serving Size",
        "Quality And Format", "Prep And Cooking Instructions",
        "Storage And Usage", "Additional Information", "Culinary Applications",
        "GTIN", "Manufacturer UPC", "Net Weight per Case"
    ]
    with open("allproducts.csv", mode="w", newline="", encoding="utf-8-sig") as f:
        writer = pd.DataFrame(columns=fieldnames)
        writer.to_csv(f, index=False)

    include_header = True
    for category_id, category_name in categories:
        print(f"\nStarting category: {category_name}")
        process_category(category_id, category_name, writer=None, include_header=False)
        include_header = False

    print("✅ Scraping complete.")
