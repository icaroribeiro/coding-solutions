import swaggerAutogen from "swagger-autogen";

const doc = {
	info: {
		title: "[MY_API] API",
		description: "[MY_API] API Documentation",
		version: "1.0.0",
		termsOfService: "http://swagger.io/terms/",
		contact: {
			email: "email@email.com",
		},
		license: {
			name: "Apache 2.0",
			url: "http://www.apache.org/licenses/LICENSE-2.0.html",
		},
	},
	host: "api.swagger.io",
	basePath: "/v1",
	tags: [
		{
			name: "purchase-order",
			description: "Purchase Order related operations",
		},
	],
	schemes: ["https"],
	paths: {
		"/purchase-order": {
			post: {
				tags: ["purchase-order"],
				summary: "Store a new purhcase order",
				description: "",
				operationId: "storePurchaseOrder",
				consumes: ["application/json"],
				produces: ["application/json"],
				parameters: [
					{
						in: "body",
						name: "body",
						description: "Purchase Order object that needs to be stored",
						required: true,
						schema: {
							$ref: "#/definitions/PurchaseOrder",
						},
					},
				],
				responses: {
					"200": {
						description: "Successful Operation",
						schema: {
							type: "string",
							items: {
								$ref: "#/definitions/ApiResponse",
							},
						},
					},
					"500": {
						description: "Internal Server Error",
						schema: {
							type: "string",
							items: {
								$ref: "#/definitions/ApiErrorResponse",
							},
						},
					},
				},
				security: [
					{
						purchase_order_auth: ["write:purchase-order"],
					},
				],
			},
		},
	},
	securityDefinitions: {
		purchase_order_auth: {
			type: "oauth2",
			authorizationUrl: "http://petstore.swagger.io/oauth/dialog",
			flow: "implicit",
			scopes: {
				"write:purchase-order": "perform purchase orders",
			},
		},
	},
	definitions: {
		Order: {
			prop1: "prop1",
		},
		PurchaseOrder: {
			prop1: "prop1",
			prop2: 10,
			prop3: 10.5,
			prop4: true,
			prop5: [
				{
					prop6: "prop6",
				},
			],
			prop7: {
				$ref: "#/definitions/Order",
			},
		},
		ApiResponse: {
			message: "message",
		},
		ApiErrorResponse: {
			message: "message",
		},
	},
};

const outputFile = "./dist/swagger.json";

swaggerAutogen(outputFile, [], doc);
