import model.*;
public class DocumentGapProbe {
    public static void main(String[] args) {
        Main.createSampleData();
        Main.menus.get(0).getCurrentRecipe().getIngredients().get(0).adjustStock(0, "audit", Main.manager);
        Order order = new Order("AUDIT", Main.tables.get(0), new Customer("CUSTOMER"));
        order.addItem(Main.menus.get(0), 1, "", "");
        System.out.println("OUT_OF_STOCK_MENU_CAN_ENTER_CART=" + (order.getItems().size() == 1));
        try { order.confirm(); } catch (IllegalArgumentException e) {
            System.out.println("OUT_OF_STOCK_REJECTED_AT_CONFIRM=true");
        }
        Menu noSop = new Menu("M", "No SOP", 20, "Food", "ครัวร้อน");
        Recipe recipe = new Recipe("R", 1);
        recipe.addIngredient(Main.ingredients.get(1), 1);
        recipe.complete();
        noSop.addRecipe(recipe);
        noSop.openSale();
        System.out.println("NO_SOP_MENU_CAN_OPEN_SALE=" + noSop.getStatus().equals("เปิดขาย"));
        System.out.println("NO_SOP_MENU_HAS_SOP=" + (Main.findSop(noSop) != null));
    }
}
