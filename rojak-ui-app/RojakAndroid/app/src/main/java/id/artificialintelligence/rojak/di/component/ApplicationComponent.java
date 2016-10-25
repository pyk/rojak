package id.artificialintelligence.rojak.di.component;

import android.content.Context;

import org.greenrobot.eventbus.EventBus;

import javax.inject.Singleton;

import dagger.Component;
import id.artificialintelligence.rojak.RojakBaseApplication;
import id.artificialintelligence.rojak.data.local.PreferencesHelper;
import id.artificialintelligence.rojak.data.remote.ApiService;
import id.artificialintelligence.rojak.data.remote.UnauthorisedInterceptor;
import id.artificialintelligence.rojak.di.module.ApplicationModule;
import id.artificialintelligence.rojak.di.module.NetworkModule;

@Singleton
@Component(modules = {
        ApplicationModule.class,
        NetworkModule.class
})
public interface ApplicationComponent {

    void inject(RojakBaseApplication baseApplication);

    void inject(UnauthorisedInterceptor unauthorisedInterceptor);

    Context context();

    ApiService apiService();

    EventBus eventBus();

    PreferencesHelper prefsHelper();

}
