import { ROUTES } from "src/common/constants/routes";
import {
  BLUEPRINT_SAFE_TYPE_OPTIONS,
  TEST_ENV,
  TEST_URL,
} from "tests/common/constants";
import { goToPage, login, tryUntil } from "tests/utils/helpers";
import { getTestID, getText } from "tests/utils/selectors";

const describeIfDeployed =
  TEST_ENV.includes("local") || TEST_ENV === "prod" ? describe.skip : describe;

const TEST_COLLECTION = {
  contactEmail: "TEST@example.com",
  contactName: "TEST NAME",
  description: "TEST DESCRIPTION",
  name: "TEST COLLECTION",
};

describe("Collection", () => {
  describeIfDeployed("Logged In Tests", () => {
    it("creates and deletes a collection", async () => {
      const timestamp = Date.now();
      await login();

      const collectionId = await createCollection(String(timestamp));

      // Try delete
      await page.click(getTestID("collection-more-button"));
      await page.click(getText("Delete Collection"));

      await page.click(".bp3-alert-footer >> text=Delete Collection");

      await goToPage(
        TEST_URL + ROUTES.PRIVATE_COLLECTION.replace(":id", collectionId)
      );

      await tryUntil(async () => {
        await expect(page).not.toHaveSelector(
          getText(TEST_COLLECTION.name + timestamp)
        );
      }, 5);
    });

    describe("Publish a collection", () => {
      describe("when no dataset", () => {
        it("shows disabled publish button", async () => {
          await login();

          await createCollection();

          const publishButton = await page.$(
            getTestID("publish-collection-button")
          );

          expect(await publishButton?.getAttribute("disabled")).toBe("");
        });
      });
    });
  });
});

async function createCollection(unique?: string): Promise<string> {
  await page.click(getText("Create Collection"));

  const collectionName = TEST_COLLECTION.name + unique;
  await page.type("#name", collectionName, BLUEPRINT_SAFE_TYPE_OPTIONS);
  await page.type(
    "#description",
    TEST_COLLECTION.description,
    BLUEPRINT_SAFE_TYPE_OPTIONS
  );
  await page.type(
    "#contact-name",
    TEST_COLLECTION.contactName,
    BLUEPRINT_SAFE_TYPE_OPTIONS
  );
  await page.type(
    "#contact-email",
    TEST_COLLECTION.contactEmail,
    BLUEPRINT_SAFE_TYPE_OPTIONS
  );
  await page.click(getText("I agree to cellxgene's data submission policies."));
  const [response] = await Promise.all([
    page.waitForEvent("response"),
    page.click(getTestID("create-button")),
  ]);

  const { collection_uuid } = (await response.json()) as {
    collection_uuid: string;
  };

  await expect(page).toHaveSelector(getText(collectionName));

  return collection_uuid;
}
