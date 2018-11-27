System.register("app", [], function(exports_1, context_1) {
    "use strict";
    var __moduleName = context_1 && context_1.id;
    var App;
    return {
        setters:[],
        execute: function() {
            App = (function () {
                function App() {
                    console.log("App loaded");
                }
                ;
                return App;
            }());
            exports_1("App", App);
            ;
        }
    }
});
//# sourceMappingURL=app.js.map