import os
import json
import urllib.parse
import datetime
from http.server import BaseHTTPRequestHandler

# In-memory storage for Vercel Serverless environment
# Note: Serverless environments may spin up new instances; state is held in-memory per instance.
ACTIVE_ORDERS = []
COMPLETED_ORDERS = []
TOKEN_COUNTER = 101

DEFAULT_MENU = [
    {"type": "Food", "id": 101, "name": "Masala Dosa", "price": 60.0, "categoryId": 1, "category": "Breakfast", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Medium", "prepTimeMinutes": 8, "stock": 40, "available": True},
    {"type": "Food", "id": 102, "name": "Idli Sambar (2 pcs)", "price": 40.0, "categoryId": 1, "category": "Breakfast", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Mild", "prepTimeMinutes": 5, "stock": 45, "available": True},
    {"type": "Food", "id": 103, "name": "Indori Poha with Sev", "price": 35.0, "categoryId": 1, "category": "Breakfast", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Mild", "prepTimeMinutes": 4, "stock": 45, "available": True},
    {"type": "Food", "id": 104, "name": "Aloo Paratha with Curd", "price": 50.0, "categoryId": 1, "category": "Breakfast", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Medium", "prepTimeMinutes": 10, "stock": 35, "available": True},
    {"type": "Food", "id": 201, "name": "Special Veg Thali", "price": 120.0, "categoryId": 2, "category": "Main Course", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Medium", "prepTimeMinutes": 12, "stock": 30, "available": True},
    {"type": "Food", "id": 202, "name": "Hyderabadi Chicken Biryani", "price": 160.0, "categoryId": 2, "category": "Main Course", "dietaryId": 1, "dietary": "Non-Veg", "spiceLevel": "Spicy", "prepTimeMinutes": 10, "stock": 35, "available": True},
    {"type": "Food", "id": 203, "name": "Paneer Butter Masala + Naan", "price": 140.0, "categoryId": 2, "category": "Main Course", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Medium", "prepTimeMinutes": 12, "stock": 25, "available": True},
    {"type": "Food", "id": 204, "name": "Dilli Rajma Chawal Bowl", "price": 80.0, "categoryId": 2, "category": "Main Course", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Medium", "prepTimeMinutes": 6, "stock": 40, "available": True},
    {"type": "Food", "id": 301, "name": "Crispy Samosa (2 pcs)", "price": 30.0, "categoryId": 3, "category": "Snacks", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Spicy", "prepTimeMinutes": 3, "stock": 60, "available": True},
    {"type": "Food", "id": 302, "name": "Veg Cheese Grilled Sandwich", "price": 70.0, "categoryId": 3, "category": "Snacks", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Mild", "prepTimeMinutes": 7, "stock": 30, "available": True},
    {"type": "Food", "id": 303, "name": "Paneer Tikka Kathi Roll", "price": 85.0, "categoryId": 3, "category": "Snacks", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Spicy", "prepTimeMinutes": 8, "stock": 25, "available": True},
    {"type": "Food", "id": 304, "name": "Peri Peri French Fries", "price": 65.0, "categoryId": 3, "category": "Snacks", "dietaryId": 2, "dietary": "Vegan", "spiceLevel": "Spicy", "prepTimeMinutes": 6, "stock": 40, "available": True},
    {"type": "Beverage", "id": 401, "name": "Adrak Masala Chai", "price": 15.0, "categoryId": 4, "category": "Beverages", "isHot": True, "volumeMl": 150, "caffeine": True, "stock": 95, "available": True},
    {"type": "Beverage", "id": 402, "name": "South Indian Filter Coffee", "price": 25.0, "categoryId": 4, "category": "Beverages", "isHot": True, "volumeMl": 180, "caffeine": True, "stock": 80, "available": True},
    {"type": "Beverage", "id": 403, "name": "Thick Cold Coffee w/ Cream", "price": 55.0, "categoryId": 4, "category": "Beverages", "isHot": False, "volumeMl": 300, "caffeine": True, "stock": 50, "available": True},
    {"type": "Beverage", "id": 404, "name": "Chilled Fresh Lime Soda", "price": 35.0, "categoryId": 4, "category": "Beverages", "isHot": False, "volumeMl": 250, "caffeine": False, "stock": 60, "available": True},
    {"type": "Food", "id": 501, "name": "Hot Gulab Jamun (2 pcs)", "price": 40.0, "categoryId": 5, "category": "Desserts", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Mild", "prepTimeMinutes": 2, "stock": 40, "available": True},
    {"type": "Food", "id": 502, "name": "Warm Brownie with Vanilla", "price": 75.0, "categoryId": 5, "category": "Desserts", "dietaryId": 0, "dietary": "Veg", "spiceLevel": "Mild", "prepTimeMinutes": 4, "stock": 25, "available": True},
    {"type": "Combo", "id": 601, "name": "Campus Hunger Buster Combo", "price": 160.0, "categoryId": 6, "category": "Combos", "originalPrice": 190.0, "includedItems": ["Veg Cheese Sandwich", "Peri Peri Fries", "Cold Coffee"], "stock": 20, "available": True},
    {"type": "Combo", "id": 602, "name": "Morning South Indian Combo", "price": 95.0, "categoryId": 6, "category": "Combos", "originalPrice": 115.0, "includedItems": ["Masala Dosa", "Idli (1 pc)", "Filter Coffee"], "stock": 25, "available": True}
]

def load_menu():
    # Attempt to load from data/menu.txt if file is present
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    menu_file = os.path.join(base_dir, "data", "menu.txt")
    if not os.path.exists(menu_file):
        return DEFAULT_MENU
    items = []
    category_names = {1: "Breakfast", 2: "Main Course", 3: "Snacks", 4: "Beverages", 5: "Desserts", 6: "Combos"}
    dietary_names = {0: "Veg", 1: "Non-Veg", 2: "Vegan"}
    try:
        with open(menu_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(";")
                item_type = parts[0]
                if item_type == "FOOD" and len(parts) >= 10:
                    cat_id = int(parts[4])
                    diet_id = int(parts[5])
                    items.append({
                        "type": "Food", "id": int(parts[1]), "name": parts[2], "price": float(parts[3]),
                        "categoryId": cat_id, "category": category_names.get(cat_id, "General"),
                        "dietaryId": diet_id, "dietary": dietary_names.get(diet_id, "Veg"),
                        "spiceLevel": parts[6], "prepTimeMinutes": int(parts[7]), "stock": int(parts[8]),
                        "available": bool(int(parts[9]) and int(parts[8]) > 0)
                    })
                elif item_type == "BEV" and len(parts) >= 10:
                    cat_id = int(parts[4])
                    items.append({
                        "type": "Beverage", "id": int(parts[1]), "name": parts[2], "price": float(parts[3]),
                        "categoryId": cat_id, "category": category_names.get(cat_id, "Beverages"),
                        "isHot": bool(int(parts[5])), "volumeMl": int(parts[6]), "caffeine": bool(int(parts[7])),
                        "stock": int(parts[8]), "available": bool(int(parts[9]) and int(parts[8]) > 0)
                    })
                elif item_type == "COMBO" and len(parts) >= 8:
                    cat_id = int(parts[4])
                    sub_items = [s.strip() for s in parts[6].split(",") if s.strip()]
                    avail = bool(int(parts[8])) if len(parts) >= 9 else True
                    items.append({
                        "type": "Combo", "id": int(parts[1]), "name": parts[2], "price": float(parts[3]),
                        "categoryId": cat_id, "category": category_names.get(cat_id, "Combos"),
                        "originalPrice": float(parts[5]), "includedItems": sub_items,
                        "stock": int(parts[7]), "available": bool(avail and int(parts[7]) > 0)
                    })
        return items if items else DEFAULT_MENU
    except Exception:
        return DEFAULT_MENU

class handler(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        global ACTIVE_ORDERS, COMPLETED_ORDERS
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Normalize path
        if path.startswith("/api/"):
            endpoint = path[5:]
        elif path == "/api":
            endpoint = "menu"
        else:
            endpoint = path.lstrip("/")

        if endpoint == "menu":
            menu_data = load_menu()
            self.send_json(200, {"success": True, "count": len(menu_data), "items": menu_data})

        elif endpoint == "tokens":
            self.send_json(200, {
                "success": True,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "activeCount": len(ACTIVE_ORDERS),
                "completedCount": len(COMPLETED_ORDERS),
                "activeOrders": ACTIVE_ORDERS,
                "completedOrders": COMPLETED_ORDERS[:15]
            })

        elif endpoint == "token_status":
            token_query = query.get("token", [""])[0].strip().upper()
            if not token_query:
                self.send_json(400, {"success": False, "error": "Missing token parameter"})
                return
            token_num = None
            if token_query.startswith("TK-") and token_query[3:].isdigit():
                token_num = int(token_query[3:])
            elif token_query.isdigit():
                token_num = int(token_query)

            found = None
            for ord_data in ACTIVE_ORDERS:
                if ord_data["tokenNumber"] == token_num or ord_data["orderId"] == token_query:
                    found = ord_data
                    break
            if not found:
                for ord_data in COMPLETED_ORDERS:
                    if ord_data["tokenNumber"] == token_num or ord_data["orderId"] == token_query:
                        found = ord_data
                        break
            if found:
                self.send_json(200, {"success": True, "order": found})
            else:
                self.send_json(404, {"success": False, "error": f"Token '{token_query}' not found."})

        elif endpoint == "analytics":
            total_orders = len(ACTIVE_ORDERS) + len(COMPLETED_ORDERS)
            revenue = sum(o.get("grandTotal", 0) for o in ACTIVE_ORDERS + COMPLETED_ORDERS)
            self.send_json(200, {
                "success": True,
                "totalOrders": total_orders,
                "activeCooking": len([o for o in ACTIVE_ORDERS if o.get("statusCode") in (1, 2)]),
                "readyForPickup": len([o for o in ACTIVE_ORDERS if o.get("statusCode") == 3]),
                "completedOrders": len(COMPLETED_ORDERS),
                "totalRevenue": round(revenue, 2)
            })

        else:
            self.send_json(404, {"success": False, "error": f"Endpoint '{endpoint}' not found"})

    def do_POST(self):
        global ACTIVE_ORDERS, COMPLETED_ORDERS, TOKEN_COUNTER
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/"):
            endpoint = path[5:]
        else:
            endpoint = path.lstrip("/")

        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            payload = json.loads(post_body.decode("utf-8"))
        except Exception:
            payload = {}

        if endpoint in ("order", "orders"):
            cust_name = payload.get("customerName", "Guest Student")
            cust_role = payload.get("customerRole", "Student")
            cust_contact = payload.get("contact", "9876543210")
            cust_id = payload.get("userId", "STU-999")
            cart_items = payload.get("items", [])
            coupon_code = payload.get("couponCode", "").strip().upper()
            pay_method = payload.get("paymentMethod", "UPI QR")

            if not cart_items:
                self.send_json(400, {"success": False, "error": "Cart cannot be empty"})
                return

            subtotal = sum(float(it.get("price", 0)) * int(it.get("quantity", 1)) for it in cart_items)
            total_qty = sum(int(it.get("quantity", 1)) for it in cart_items)
            user_discount_rate = 0.05 if cust_role == "Student" else (0.10 if cust_role == "Faculty" else 0.0)
            user_discount = round(subtotal * user_discount_rate, 2)

            coupon_discount = 0.0
            if coupon_code == "CAMPUS50" and subtotal >= 200:
                coupon_discount = 50.0
            elif coupon_code == "WELCOME10":
                coupon_discount = round(subtotal * 0.10, 2)
            elif coupon_code == "SNACK5" and subtotal >= 50:
                coupon_discount = 5.0

            taxable = max(0.0, subtotal - user_discount - coupon_discount)
            canteen_tax = round(taxable * 0.05, 2)
            grand_total = round(taxable + canteen_tax, 2)

            token_num = TOKEN_COUNTER
            TOKEN_COUNTER += 1

            prep_minutes = max(5, min(35, 5 + total_qty * 2))
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_id = f"ORD-{int(datetime.datetime.now().timestamp())}-{token_num}"
            pay_ref = f"TXN-VERCEL-{token_num}"

            order_record = {
                "orderId": order_id,
                "tokenNumber": token_num,
                "timestamp": now_str,
                "customer": {"name": cust_name, "role": cust_role, "contact": cust_contact, "id": cust_id},
                "items": cart_items,
                "subtotal": subtotal,
                "userDiscount": user_discount,
                "couponDiscount": coupon_discount,
                "couponCode": coupon_code,
                "tax": canteen_tax,
                "grandTotal": grand_total,
                "status": "Order Placed",
                "statusCode": 1,
                "prepMinutes": prep_minutes,
                "payment": {"method": pay_method, "reference": pay_ref}
            }
            ACTIVE_ORDERS.insert(0, order_record)
            self.send_json(200, {"success": True, "order": order_record})

        elif endpoint == "advance_token":
            token_num = payload.get("tokenNumber")
            if not token_num:
                self.send_json(400, {"success": False, "error": "Missing tokenNumber"})
                return

            target = None
            for ord_data in ACTIVE_ORDERS:
                if ord_data["tokenNumber"] == token_num:
                    target = ord_data
                    break

            if not target:
                self.send_json(404, {"success": False, "error": "Active order not found"})
                return

            prev_code = target["statusCode"]
            if prev_code == 1:
                target["statusCode"] = 2
                target["status"] = "In Kitchen / Preparing"
            elif prev_code == 2:
                target["statusCode"] = 3
                target["status"] = "Ready for Pickup"
            elif prev_code == 3:
                target["statusCode"] = 4
                target["status"] = "Completed"
                ACTIVE_ORDERS.remove(target)
                COMPLETED_ORDERS.insert(0, target)

            self.send_json(200, {
                "success": True,
                "tokenNumber": token_num,
                "newStatus": target["status"],
                "statusCode": target["statusCode"]
            })

        else:
            self.send_json(404, {"success": False, "error": "Endpoint not found"})
