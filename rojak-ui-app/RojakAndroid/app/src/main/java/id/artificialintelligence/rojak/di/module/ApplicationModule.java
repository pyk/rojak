package id.artificialintelligence.rojak.di.module;

import android.content.Context;

import org.greenrobot.eventbus.EventBus;

import javax.inject.Singleton;

import dagger.Module;
import dagger.Provides;
import id.artificialintelligence.rojak.RojakBaseApplication;
import id.artificialintelligence.rojak.data.local.PreferencesHelper;

@Module
public class ApplicationModule {

    private final RojakBaseApplication mBaseApplication;

    public ApplicationModule(RojakBaseApplication baseApplication) {
        this.mBaseApplication = baseApplication;
    }

    @Provides
    Context provideContext(){
        return mBaseApplication;
    }

    @Provides
    @Singleton
    public RojakBaseApplication provideApplication() {
        return mBaseApplication;
    }

    @Provides
    @Singleton
    public EventBus eventBus() {
        return new EventBus();
    }

    @Provides
    @Singleton
    public PreferencesHelper prefsHelper() {
        return new PreferencesHelper(mBaseApplication);
    }

}
